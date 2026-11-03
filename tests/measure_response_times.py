import csv,json,time,urllib.request,uuid
from decimal import Decimal,ROUND_HALF_UP
from test_support import RUN,now
from test_api_and_accounting import Client,sql,save,ACCOUNTING

c=Client();c.login()
stations=c.call('GET','/api/v1/stations?country=MY&cpoId=cpo_voltgo')[1]
uid=next(k['evseUid'] for s in stations if s['isSimulated'] for k in s['connectors'] if k['status']=='AVAILABLE' and k['powerType']=='DC')
q=c.call('POST','/api/v1/quotes',dict(evseUid=uid,estimatedKwh='15'))[1]
started=now();clock=time.perf_counter()
code,s,_=c.call('POST','/api/v1/sessions/start',dict(evseUid=uid,quoteId=q['id'],targetSoc=100),{'Idempotency-Key':uuid.uuid4().hex});assert code==201
frames=[]
req=urllib.request.Request('http://localhost:18080/api/v1/sessions/'+s['id']+'/stream',headers={'Authorization':'Bearer '+c.token})
with urllib.request.urlopen(req,timeout=25) as stream:
    event=''
    while time.perf_counter()-clock<20:
        line=stream.readline().decode().strip()
        if line.startswith('event:'):event=line[6:].strip()
        if line.startswith('data:'):
            row=json.loads(line[5:]);frames.append(dict(at=now(),event=event,session=row))
            if row.get('kwhDelivered',0)>0:break
assert frames[-1]['session']['kwhDelivered']>0
save('evidence/performance/tc43-start-to-first-sse.json',dict(start_request_sent_at=started,first_positive_telemetry_at=now(),elapsed_ms=(time.perf_counter()-clock)*1000,session_id=s['id'],frames=frames,method='monotonic clock begins before POST start; ends at first received positive-energy SSE frame'))
assert c.call('POST','/api/v1/sessions/'+s['id']+'/stop')[0]==200
from export_session_accounting import export
export()
