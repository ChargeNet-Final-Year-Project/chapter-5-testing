import os
import base64
import csv
import http.cookiejar
import io
import json
import math
from pathlib import Path
import socket
import statistics
import subprocess
import threading
import time
import urllib.error
import urllib.request
import uuid
from test_support import ROOT,RUN,DB_CONTAINER,RUNTIME_DSN,now,validate_runtime_dsn

BASE=os.environ.get('API_BASE_URL','http://localhost:18080').rstrip('/')
records=[]

def scrub(value):
    if isinstance(value,dict):
        return {k:('[REDACTED]' if k.lower().replace('_','') in ['token','tokena','tokenb','tokenc','password','passwordhash','accountno','bankaccountno','accountnumber','signingsecret'] else scrub(v)) for k,v in value.items()}
    if isinstance(value,list):return [scrub(x) for x in value]
    return value

def save(path,value):
    p=RUN/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(scrub(value),indent=2,default=str),encoding='utf8')

def sql(query,output=None):
    validate_runtime_dsn(RUNTIME_DSN)
    p=subprocess.run(['docker','exec','-i',DB_CONTAINER,'psql','-U','chargenet','-d',os.environ.get('CHARGENET_RUNTIME_DB','chargenet_evidence_test'),'--csv','-v','ON_ERROR_STOP=1'],input=query,text=True,capture_output=True)
    if output:
        dest=RUN/output;dest.parent.mkdir(parents=True,exist_ok=True)
        dest.with_suffix('.sql').write_text(query,encoding='utf8');dest.write_text(p.stdout,encoding='utf8')
    if p.returncode:raise RuntimeError(p.stderr)
    return list(csv.DictReader(io.StringIO(p.stdout)))

class Client:
    def __init__(self):
        self.token=None
        self.jar=http.cookiejar.CookieJar()
        self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
    def call(self,method,path,body=None,headers=None,record=True):
        h={'Content-Type':'application/json',**(headers or {})}
        if self.token:h['Authorization']='Bearer '+self.token
        raw=None if body is None else json.dumps(body).encode()
        req=urllib.request.Request(BASE+path,raw,h,method=method)
        start=now();clock=time.perf_counter()
        try:r=self.opener.open(req,timeout=35)
        except urllib.error.HTTPError as e:r=e
        data=r.read().decode();status=r.status
        try:data=json.loads(data)
        except ValueError:pass
        if record:records.append(dict(method=method,path=path,started_at=start,finished_at=now(),status=status,response=scrub(data),elapsed_ms=(time.perf_counter()-clock)*1000))
        return status,data,dict(r.headers)
    def login(self,email='demo@chargenet.my',password=os.environ.get('CHARGENET_DRIVER_PASSWORD', '')):
        code,data,_=self.call('POST','/api/v1/auth/login',dict(email=email,password=password));assert code==200,(code,data)
        self.token=data['token'];return data

def positive_session(client,country='MY',cpo='cpo_voltgo'):
    code,stations,_=client.call('GET',f'/api/v1/stations?country={country}&cpoId={cpo}');assert code==200
    station,connector=next((s,c) for s in stations if s['isSimulated'] for c in s['connectors'] if c['powerType']=='DC' and c['status']=='AVAILABLE')
    code,q,_=client.call('POST','/api/v1/quotes',dict(evseUid=connector['evseUid'],estimatedKwh='15'));assert code==201,(code,q)
    code,s,_=client.call('POST','/api/v1/sessions/start',dict(evseUid=connector['evseUid'],quoteId=q['id'],targetSoc=100),{'Idempotency-Key':str(uuid.uuid4())});assert code==201,(code,s)
    first=None;start=time.perf_counter()
    for _ in range(100):
        _,s,_=client.call('GET','/api/v1/sessions/'+s['id'])
        if s['kwhDelivered']>0:first=(time.perf_counter()-start)*1000;break
        time.sleep(.1)
    assert first is not None
    return s,q,first

ACCOUNTING="""SELECT s.id AS session_id,s.user_id,s.status,s.kwh_delivered,s.original_currency,s.original_cost,s.wallet_currency,s.exchange_rate,s.tariff_per_kwh,s.total_cost,s.balance_after,(SELECT q.budget FROM charging_quotes q WHERE q.id=s.quote_id) AS accepted_budget,s.unfunded_amount,c.id AS cdr_id,s.cdr_id AS legacy_session_cdr_id,
 (SELECT count(*) FROM cdrs c WHERE c.session_id=s.id) AS cdr_count,
 (SELECT count(*) FROM wallet_transactions t WHERE t.session_id=s.id AND t.type='CHARGING_DEBIT') AS debit_count,
 (SELECT coalesce(sum(t.amount),0) FROM wallet_transactions t WHERE t.session_id=s.id AND t.type='CHARGING_DEBIT') AS debit_amount,
 w.balance,(SELECT coalesce(sum(r.amount),0) FROM wallet_reservations r WHERE r.wallet_id=w.id AND r.status='HELD') AS reserved,k.status AS connector_status,c.currency AS cdr_currency,c.gross_amount,c.platform_fee,c.net_payout
 FROM charging_sessions s JOIN wallets w ON w.user_id=s.user_id JOIN connectors k ON k.id=s.connector_id LEFT JOIN cdrs c ON c.session_id=s.id
 WHERE s.id NOT LIKE 'report_%' AND s.user_id<>'usr_sandbox' ORDER BY s.start_time;"""

def run_checks():
    c=Client();health=c.call('GET','/healthz');assert health[0]==200 and health[1]['db']=='up'
    c.login();_,me,_=c.call('GET','/api/v1/auth/me');save('evidence/integration/tc09-same-driver.json',me)
    _,stations,_=c.call('GET','/api/v1/stations')
    samples=[]
    for i in range(35):
        start=now();clock=time.perf_counter();status,data,_=c.call('GET','/api/v1/stations',record=False)
        samples.append(dict(sample=i+1,warmup=i<5,started_at=start,http_status=status,elapsed_ms=(time.perf_counter()-clock)*1000,station_count=len(data)))
    with (RUN/'evidence/performance/timing-samples.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(samples[0]));w.writeheader();w.writerows(samples)
    times=[x['elapsed_ms'] for x in samples[5:] if x['http_status']==200]
    save('evidence/performance/timing-summary.json',dict(warmups=5,sample_count=30,median_ms=statistics.median(times),p95_ms=sorted(times)[math.ceil(.95*len(times))-1],p95_method='nearest rank: sorted successful samples at ceil(0.95*n)',errors=[x for x in samples[5:] if x['http_status']!=200],station_count=len(stations),sla=None,scope='single local sequential client; descriptive'))

    # Lost response: send a complete request and discard its response, then replay.
    station,connector=next((s,k) for s in stations if s['isSimulated'] and s['cpoId']=='cpo_voltgo' for k in s['connectors'] if k['powerType']=='DC' and k['status']=='AVAILABLE')
    _,q,_=c.call('POST','/api/v1/quotes',dict(evseUid=connector['evseUid'],estimatedKwh='15'))
    key='dropped-response-'+uuid.uuid4().hex
    body=dict(evseUid=connector['evseUid'],quoteId=q['id'],targetSoc=100);raw=json.dumps(body).encode()
    wire=(f'POST /api/v1/sessions/start HTTP/1.1\r\nHost: localhost:18080\r\nContent-Type: application/json\r\nAuthorization: Bearer {c.token}\r\nIdempotency-Key: {key}\r\nContent-Length: {len(raw)}\r\nConnection: close\r\n\r\n').encode()+raw
    lost_at=now()
    with socket.create_connection(('127.0.0.1',18080),timeout=10) as sock:
        sock.sendall(wire)
        for _ in range(100):
            found=sql("SELECT response_status,response_body->>'id' AS session_id FROM idempotency_keys WHERE key='"+key+"';")
            if found:break
            time.sleep(.1)
        assert found,'original request did not commit'
        # Do not read a single response byte.
    status,replay,headers=c.call('POST','/api/v1/sessions/start',body,{'Idempotency-Key':key})
    assert status==201 and headers.get('Idempotent-Replay')=='true' and replay['id']==found[0]['session_id']
    for _ in range(100):
        _,live,_=c.call('GET','/api/v1/sessions/'+replay['id'])
        if live['kwhDelivered']>0:break
        time.sleep(.1)
    assert live['kwhDelivered']>0
    save('evidence/reliability/tc26-dropped-start-replay.json',dict(lost_at=lost_at,response_bytes_read=0,original=found,replay_status=status,replay_header=headers.get('Idempotent-Replay'),session_id=replay['id'],live=live))
    barrier=threading.Barrier(3);out=[]
    def stop():
        other=Client();other.token=c.token;barrier.wait();out.append(other.call('POST','/api/v1/sessions/'+replay['id']+'/stop')[:2])
    threads=[threading.Thread(target=stop) for _ in range(2)]
    for t in threads:t.start()
    barrier.wait()
    for t in threads:t.join()
    out.append(c.call('POST','/api/v1/sessions/'+replay['id']+'/stop')[:2])
    assert all(x[0]==200 and x[1]['cdrId']==out[0][1]['cdrId'] and x[1]['totalCost']==out[0][1]['totalCost'] for x in out)
    save('evidence/reliability/tc28-repeated-settlement/concurrent-stops.json',dict(session_id=replay['id'],responses=out))

    # Direct HTTP access boundaries with roles and tokens omitted from evidence.
    other=Client();code,reg,_=other.call('POST','/api/v1/auth/register',dict(name='Evidence Second Driver',email='evidence-second@example.test',password=os.environ.get('CHARGENET_FIXTURE_PASSWORD', '')))
    assert code==201,(code,reg)
    other.token=reg['token']
    denied=[]
    for path in ['/api/v1/sessions/'+replay['id'],'/api/v1/sessions/'+replay['id']+'/stream']:
        code,data,_=other.call('GET',path);denied.append(dict(role='other_driver',path=path,status=code,response=data));assert code in [403,404]
    portal=Client();assert portal.call('POST','/admin/api/login',dict(email='ops@voltgo.my',password=os.environ.get('CHARGENET_OPERATOR_PASSWORD', '')))[0]==200
    for who,client,path in [('anonymous',Client(),'/admin/api/network'),('CPO',portal,'/admin/api/admin/cpos')]:
        code,data,_=client.call('GET',path);denied.append(dict(role=who,path=path,status=code,response=data));assert code in [401,403]
    foreign=Client();assert foreign.call('POST','/admin/api/login',dict(email='ops@ecowatt.my',password=os.environ.get('CHARGENET_OPERATOR_PASSWORD', '')))[0]==200
    code,data,_=foreign.call('GET','/admin/api/cdrs/'+out[0][1]['cdrId']);denied.append(dict(role='foreign_CPO',path='/admin/api/cdrs/'+out[0][1]['cdrId'],status=code,response=data));assert code in [403,404]
    for h in [{},{'Authorization':'Token '+base64.b64encode(b'unknown-evidence-token').decode()}]:
        code,data,_=Client().call('GET','/ocpi/emsp/2.3.0/locations',headers=h);denied.append(dict(role='missing_or_unknown_OCPI_token',path='/ocpi/emsp/2.3.0/locations',status=code,response=data));assert code in [401,403]
    save('evidence/requests/tc36-tc37-tc38-access-denials.json',denied)
    # Inspect the payload itself, using operational token values only in memory.
    _,profile,_=portal.call('GET','/admin/api/cpo')
    secrets=sql("SELECT token_b,token_c FROM cpo_partners WHERE id='cpo_voltgo';")[0]
    payload=json.dumps(profile)
    assert all(v not in payload for v in secrets.values() if v)
    save('evidence/integration/tc13-operational-token-payload-check.json',dict(role='VoltGo CPO',full_operational_tokens_present=False,profile=scrub(profile)))
    # Advertised directions and modules, authenticated with disposable Token C.
    h={'Authorization':'Token '+base64.b64encode(secrets['token_c'].encode()).decode()}
    for suffix,name in [('versions','TC17_versions'),('2.3.0','TC17_modules')]:
        code,data,_=Client().call('GET','/ocpi/emsp/'+suffix,headers=h);save('evidence/integration/'+name+'.json',dict(status=code,response=data));assert code==200

    # The real emulator rejects and becomes unreachable, then its knobs are restored.
    fault_results=[]
    for knob in ['reject_next','offline']:
        c.call('POST','/emulator/voltgo/ocpi/admin/scenario',{knob:True})
        _,q,_=c.call('POST','/api/v1/quotes',dict(evseUid=connector['evseUid'],estimatedKwh='15'))
        before=c.call('GET','/api/v1/wallet')[1]
        code,data,_=c.call('POST','/api/v1/sessions/start',dict(evseUid=connector['evseUid'],quoteId=q['id'],targetSoc=100),{'Idempotency-Key':uuid.uuid4().hex})
        after=c.call('GET','/api/v1/wallet')[1]
        assert code>=400 and before['balance']==after['balance'] and after['reserved']==0
        fault_results.append(dict(knob=knob,status=code,response=data,walletBefore=before,walletAfter=after))
        c.call('POST','/emulator/voltgo/ocpi/admin/scenario',dict(offline=False,reject_next=False,fault_after_seconds=0))
    save('evidence/reliability/TC29_real_ocpi_start_failures.json',fault_results)
    sql(ACCOUNTING,'evidence/database/tc28-session-cdr-wallet.csv')
    save('evidence/requests/test_api_and_accounting.json',records)
    print('Runtime checks completed',flush=True)

def export_accounting():
    sql(ACCOUNTING,'evidence/database/tc28-session-cdr-wallet.csv')
    print('Accounting export complete')

def restart_checks():
    c=Client();c.login()
    before,q,delay=positive_session(c)
    save('evidence/reliability/tc31-active-restart/before.json',dict(captured_at=now(),session=before,quote=q,start_to_first_telemetry_ms=delay,process_boundary='backend and all three in-process emulators'))
    (RUN/'build/restart_backend').write_text(now())
    for _ in range(120):
        time.sleep(.25)
        try:
            if not (RUN/'build/restart_backend').exists() and Client().call('GET','/healthz')[0]==200:break
        except OSError:pass
    observed=[]
    for _ in range(100):
        code,row,_=c.call('GET','/api/v1/sessions/'+before['id']);observed.append(dict(at=now(),status=code,session=row))
        if row.get('status') in ['COMPLETED','FAILED'] or row.get('kwhDelivered',0)>before['kwhDelivered']:break
        time.sleep(.1)
    save('evidence/reliability/tc31-active-restart/after.json',dict(observations=observed,independent_cpo_persistence=False))
    if row['status'] in ['PENDING','CHARGING']:
        code,row,_=c.call('POST','/api/v1/sessions/'+before['id']+'/stop');assert code==200
    assert row['kwhDelivered']>=before['kwhDelivered'] and row['cdrId']
    save('evidence/reliability/tc31-active-restart/.json',row)
    # Durable settlement intent, captured before abrupt termination. The fixture
    # deliberately writes exactly the same intent fields the store uses.
    before,q,delay=positive_session(c)
    sql("UPDATE charging_sessions SET settlement_requested_status='COMPLETED',settlement_requested_reason='USER' WHERE id='"+before['id']+"';",'evidence/reliability/tc32-settlement-restart/intent-write.csv')
    intent=sql("SELECT id,status,kwh_delivered,original_cost,exchange_rate,settlement_requested_status,settlement_requested_reason FROM charging_sessions WHERE id='"+before['id']+"';",'evidence/reliability/tc32-settlement-restart/durable-intent.csv')
    (RUN/'build/restart_backend').write_text(now())
    for _ in range(120):
        time.sleep(.25)
        try:
            if not (RUN/'build/restart_backend').exists():
                code,row,_=c.call('GET','/api/v1/sessions/'+before['id'])
                if code==200 and row.get('cdrId'):break
        except OSError:pass
    save('evidence/reliability/tc32-settlement-restart/recovered.json',dict(intent=intent,quote=q,session=row,scope='durable intent injected in disposable SQL; delivery emulator stops at process death'))
    assert row['cdrId'] and row['exchangeRate']==q['exchangeRate']
    (RUN/'build/restart_backend').write_text(now())
    for _ in range(120):
        time.sleep(.25)
        try:
            if not (RUN/'build/restart_backend').exists() and c.call('GET','/healthz')[0]==200:break
        except OSError:pass
    sql(ACCOUNTING,'evidence/database/tc31-tc32-after-repeated-restart.csv')
    save('evidence/requests/Restart checks.json',records)
    print('Restart checks completed',flush=True)

if __name__=='__main__':
    import sys
    try:globals()[sys.argv[1]]()
    finally:save('evidence/requests/'+sys.argv[1]+'_trace.json',records)
