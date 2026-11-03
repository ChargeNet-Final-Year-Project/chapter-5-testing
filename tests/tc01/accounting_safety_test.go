package sessions_test

import (
	"context"
	"sync"
	"testing"
	"time"

	"github.com/chargenet/chargenet-backend/internal/gateway"
	"github.com/chargenet/chargenet-backend/internal/sessions"
	"github.com/chargenet/chargenet-backend/internal/store"
)

// These orchestrator tests use real PostgreSQL and an explicitly controlled
// transport. They do not establish OCPI or Android execution.
type evidenceTransport struct {
	startErr error
	stopErr  error
	onStop   func(context.Context, string) error
	events   chan gateway.Telemetry
}

func (g *evidenceTransport) StartSession(context.Context, gateway.StartCmd) error { return g.startErr }
func (g *evidenceTransport) StopSession(ctx context.Context, id string) error {
	if g.onStop != nil {
		return g.onStop(ctx, id)
	}
	return g.stopErr
}
func (g *evidenceTransport) UnlockConnector(context.Context, string) error { return nil }
func (g *evidenceTransport) Subscribe() <-chan gateway.Telemetry           { return g.events }

func evidenceManager(t *testing.T, h *harness, g gateway.CPOGateway) *sessions.Manager {
	t.Helper()
	m := sessions.NewManager(h.st, g, h.cfg)
	ctx, cancel := context.WithCancel(context.Background())
	m.Run(ctx)
	t.Cleanup(func() { cancel(); m.Shutdown() })
	return m
}

func TestEvidenceConcurrentDriversSameConnector(t *testing.T) {
	h := newHarness(t)
	g := &evidenceTransport{events: make(chan gateway.Telemetry, 8)}
	m := evidenceManager(t, h, g)
	users := []string{h.driver(100), h.driver(100)}
	quotes := make([]string, 2)
	for i, u := range users {
		q, err := h.st.CreateQuote(context.Background(), u, testEVSE, "15")
		if err != nil {
			t.Fatal(err)
		}
		quotes[i] = q.ID
	}
	type result struct {
		index   int
		session *store.Session
		err     error
	}
	ready := sync.WaitGroup{}
	ready.Add(2)
	barrier := make(chan struct{})
	results := make(chan result, 2)
	for i := range users {
		go func(i int) {
			ready.Done()
			<-barrier
			s, err := m.Start(context.Background(), users[i], sessions.StartRequest{EVSEUID: testEVSE, QuoteID: quotes[i], TargetSoC: 100})
			results <- result{i, s, err}
		}(i)
	}
	ready.Wait()
	close(barrier)
	wins := 0
	for range users {
		r := <-results
		w, err := h.st.GetWallet(context.Background(), users[r.index])
		if err != nil {
			t.Fatal(err)
		}
		debits, _ := h.debitTotals(users[r.index])
		if debits != 0 || w.Balance != 100 {
			t.Fatalf("unexpected charge: %+v debits=%d", w, debits)
		}
		var count int
		if err := h.st.DB.QueryRow(`SELECT count(*) FROM charging_sessions WHERE user_id=$1`, users[r.index]).Scan(&count); err != nil {
			t.Fatal(err)
		}
		if r.err == nil {
			wins++
			if count != 1 || w.Reserved <= 0 {
				t.Fatalf("winner missing session/hold: count=%d wallet=%+v", count, w)
			}
			t.Logf("winner session=%s user=%s reserved=%.2f", r.session.ID, users[r.index], w.Reserved)
		} else {
			wantCode(t, r.err, sessions.CodeConnectorUnavailable)
			if count != 0 || w.Reserved != 0 {
				t.Fatalf("loser retained session/hold: count=%d wallet=%+v", count, w)
			}
			t.Logf("loser user=%s sessions=%d reserved=%.2f", users[r.index], count, w.Reserved)
		}
	}
	if wins != 1 {
		t.Fatalf("winning starts=%d, want one", wins)
	}
}

func TestEvidenceZeroEnergyRepeatedStop(t *testing.T) {
	h := newHarness(t)
	// No timer tick can occur before stop: a real local simulator, zero energy.
	g := gateway.NewLocalGateway(1, gateway.WithTick(time.Hour))
	t.Cleanup(g.Close)
	m := evidenceManager(t, h, g)
	u := h.driver(100)
	s := h.start(m, u, 100)
	for range 3 {
		done, err := m.Stop(context.Background(), u, s.ID)
		if err != nil {
			t.Fatal(err)
		}
		if !done.Terminal() || done.KWhDelivered != 0 || done.TotalCost != 0 {
			t.Fatalf("zero-energy result: %+v", done)
		}
	}
	w, err := h.st.GetWallet(context.Background(), u)
	if err != nil {
		t.Fatal(err)
	}
	n, amount := h.debitTotals(u)
	var cdrs int
	if err := h.st.DB.QueryRow(`SELECT count(*) FROM cdrs WHERE session_id=$1`, s.ID).Scan(&cdrs); err != nil {
		t.Fatal(err)
	}
	if n != 0 || amount != 0 || w.Balance != 100 || w.Reserved != 0 || cdrs != 1 || h.connectorStatus(testEVSE) != store.StatusAvailable {
		t.Fatalf("zero settlement: cdrs=%d debits=%d amount=%v wallet=%+v", cdrs, n, amount, w)
	}
	t.Logf("session=%s cdrs=%d debits=%d balance=%.2f reserved=%.2f connector=AVAILABLE", s.ID, cdrs, n, w.Balance, w.Reserved)
}

func TestEvidenceStartFailureReleasesAccounting(t *testing.T) {
	for _, code := range []string{gateway.CodeConnectorUnavailable, gateway.CodeCPOUnreachable} {
		t.Run(code, func(t *testing.T) {
			h := newHarness(t)
			g := &evidenceTransport{startErr: gateway.Errorf(code, "controlled rejection or transport timeout"), events: make(chan gateway.Telemetry, 8)}
			m := evidenceManager(t, h, g)
			u := h.driver(100)
			q, err := h.st.CreateQuote(context.Background(), u, testEVSE, "15")
			if err != nil {
				t.Fatal(err)
			}
			_, err = m.Start(context.Background(), u, sessions.StartRequest{EVSEUID: testEVSE, QuoteID: q.ID, TargetSoC: 100})
			if err == nil {
				t.Fatal("failed transport start was accepted")
			}
			w, err := h.st.GetWallet(context.Background(), u)
			if err != nil {
				t.Fatal(err)
			}
			n, _ := h.debitTotals(u)
			var active, cdrs int
			if err := h.st.DB.QueryRow(`SELECT count(*) FROM charging_sessions WHERE user_id=$1 AND status IN ('PENDING','CHARGING')`, u).Scan(&active); err != nil {
				t.Fatal(err)
			}
			if err := h.st.DB.QueryRow(`SELECT count(*) FROM cdrs c JOIN charging_sessions s ON s.id=c.session_id WHERE s.user_id=$1`, u).Scan(&cdrs); err != nil {
				t.Fatal(err)
			}
			if active != 0 || n != 0 || w.Reserved != 0 || w.Balance != 100 || h.connectorStatus(testEVSE) != store.StatusAvailable {
				t.Fatalf("failed start leaked accounting: active=%d debits=%d wallet=%+v", active, n, w)
			}
			t.Logf("error=%s active=%d cdrs=%d debits=%d reserved=%.2f balance=%.2f", code, active, cdrs, n, w.Reserved, w.Balance)
		})
	}
}
