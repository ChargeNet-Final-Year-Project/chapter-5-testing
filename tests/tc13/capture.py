"""Real curl requests and read-only PostgreSQL observations for this case."""
from pathlib import Path
import datetime, json, os, subprocess, threading, time, uuid, csv, io

HERE = Path(__file__).resolve().parent
BASE = os.environ.get('API_BASE_URL', 'http://localhost:18080')
LOCK = threading.Lock()
COUNTER = 0

def note(text):
    with LOCK:
        with (HERE / 'requests.txt').open('a', encoding='utf-8', newline='') as f:
            f.write(str(text) + '\n')
        print(text, flush=True)

class Client:
    def __init__(self, name='driver'):
        self.token = None
        self.cookies = HERE / (name + '-cookies.txt')

    def call(self, method, path, body=None, headers=None, timeout=40):
        global COUNTER
        with LOCK:
            COUNTER += 1
            number = COUNTER
        args = ['curl.exe', '--silent', '--show-error', '--max-time', str(timeout), '-i', '-X', method,
                '-b', str(self.cookies), '-c', str(self.cookies), '-H', 'Content-Type: application/json']
        if self.token:
            args += ['-H', 'Authorization: Bearer ' + self.token]
        for k, v in (headers or {}).items():
            args += ['-H', k + ': ' + v]
        if body is not None:
            file = HERE / f'input-{uuid.uuid4().hex[:8]}-{number:03}.json'
            file.write_text(json.dumps(body), encoding='utf-8')
            args += ['--data-binary', '@' + file.name]
        args.append(BASE + path)
        result = subprocess.run(args, cwd=HERE, capture_output=True)
        raw = result.stdout.decode('utf-8', 'replace')
        stderr = result.stderr.decode('utf-8', 'replace')
        note('\n' + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
             + '\nRequest body: ' + (json.dumps(body) if body is not None else '(none)') + '\n$ ' + subprocess.list2cmdline(args) + '\n' + raw + stderr + '\ncurl exit: ' + str(result.returncode))
        payload = raw.split('\r\n\r\n', 1)[-1] if '\r\n\r\n' in raw else raw.split('\n\n', 1)[-1]
        try:
            return json.loads(payload)
        except ValueError:
            return payload

    def login(self, email='demo@chargenet.my', password='Demo1234!'):
        data = self.call('POST', '/api/v1/auth/login', dict(email=email, password=password))
        self.token = data['token']
        return data

    def register(self):
        email = 'ch5-' + uuid.uuid4().hex[:10] + '@example.test'
        data = self.call('POST', '/api/v1/auth/register', dict(name='Chapter Five Driver', email=email, password='LocalOnly123!'))
        self.token = data['token']
        return data

    def fund(self, amount=100):
        return self.call('POST', '/api/v1/wallet/topup', dict(amount=amount, paymentMethod='Credit Card'), {'Idempotency-Key': uuid.uuid4().hex})

    def pick(self, country='MY', cpo='cpo_voltgo', power='DC'):
        stations = self.call('GET', '/api/v1/stations?country=' + country + '&cpoId=' + cpo)
        return next((s, k) for s in stations if s['isSimulated'] for k in s['connectors'] if k['powerType'] == power and k['status'] == 'AVAILABLE')

    def quote(self, connector):
        return self.call('POST', '/api/v1/quotes', dict(evseUid=connector['evseUid'], estimatedKwh='15'))

    def start(self, connector, quote, key=None):
        return self.call('POST', '/api/v1/sessions/start', dict(evseUid=connector['evseUid'], quoteId=quote['id'], targetSoc=100), {'Idempotency-Key': key or uuid.uuid4().hex})

    def positive(self, session):
        for _ in range(30):
            current = self.call('GET', '/api/v1/sessions/' + session['id'])
            if current.get('kwhDelivered', 0) > 0:
                return current
            time.sleep(1)
        raise RuntimeError('No positive telemetry observed within 30 seconds')

def sql(query):
    args = ['docker', 'exec', '-i', 'chargenet-ch5-new-postgres', 'psql', '-U', 'chargenet', '-d', 'chargenet_evidence_test', '--csv', '-v', 'ON_ERROR_STOP=1', '-c', query]
    result = subprocess.run(args, capture_output=True)
    note('\n$ ' + subprocess.list2cmdline(args) + '\n' + result.stdout.decode('utf-8', 'replace') + result.stderr.decode('utf-8', 'replace') + '\nexit: ' + str(result.returncode))
    return list(csv.DictReader(io.StringIO(result.stdout.decode('utf-8', 'replace'))))

def accounting(sid):
    return sql("SELECT s.id,s.user_id,s.status,s.kwh_delivered,s.original_currency,s.original_cost,s.wallet_currency,s.total_cost,s.exchange_rate,s.tariff_per_kwh,k.status AS connector_status,(SELECT count(*) FROM cdrs c WHERE c.session_id=s.id) AS cdr_count,(SELECT count(*) FROM wallet_transactions t WHERE t.session_id=s.id AND t.type='CHARGING_DEBIT') AS debit_count,(SELECT coalesce(sum(amount),0) FROM wallet_reservations r WHERE r.wallet_id=w.id AND r.status='HELD') AS reserved,w.balance FROM charging_sessions s JOIN wallets w ON w.user_id=s.user_id JOIN connectors k ON k.id=s.connector_id WHERE s.id='" + sid + "';")
