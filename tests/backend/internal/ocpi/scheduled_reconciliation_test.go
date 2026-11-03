package ocpi_test

import (
	"context"
	"net/http"
	"sync/atomic"
	"testing"
	"time"

	"github.com/chargenet/chargenet-backend/internal/ocpi"
	"github.com/chargenet/chargenet-backend/internal/testutil"
)

// Controlled real HTTP partner, real SQL store and real scheduled ticker.
// No push is sent. 50 ms is an accelerated test interval; production is 5 min.
func TestEvidenceScheduledSyncRepairsMissedPush(t *testing.T) {
	st := testutil.NewTestStore(t)
	var changed atomic.Bool
	locations := func(w http.ResponseWriter, r *http.Request) {
		loc := syncLocation()
		if changed.Load() {
			loc.Name = "Missed push recovered"
			loc.EVSEs[0].Status = "OUTOFORDER"
		}
		listOf([]ocpi.Location{loc})(w, r)
	}
	srv := newPartner(t, "sync-token-b", locations, listOf([]ocpi.Tariff{syncTariff()}))
	p := syncTestPartner(t, st, srv.URL)
	s := ocpi.NewSyncer(st, ocpi.WithSyncInterval(50*time.Millisecond))
	if err := s.SyncOne(context.Background(), p); err != nil {
		t.Fatal(err)
	}
	before, err := st.GetOCPILocation(context.Background(), p.ID, "SYN-9")
	if err != nil {
		t.Fatal(err)
	}
	if before.Name != "SyncTest Hub" {
		t.Fatal("initial fixture mismatch")
	}
	changedAt := time.Now()
	changed.Store(true)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	done := make(chan struct{})
	go func() { defer close(done); s.Run(ctx) }()
	defer func() { cancel(); <-done }()
	for time.Since(changedAt) < 5*time.Second {
		after, err := st.GetOCPILocation(ctx, p.ID, "SYN-9")
		if err == nil && after.Name == "Missed push recovered" && len(after.Connectors) == 1 && after.Connectors[0].Status == "INOPERATIVE" {
			t.Logf("source_changed=%s old=%s new=%s status=%s observed=%s delay_ms=%d interval_ms=50 normal_interval=5m push_sent=false", changedAt.Format(time.RFC3339Nano), before.Name, after.Name, after.Connectors[0].Status, time.Now().Format(time.RFC3339Nano), time.Since(changedAt).Milliseconds())
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatal("scheduled pull did not recover the missed push within five seconds")
}
