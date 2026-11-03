from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
from concurrent.futures import ThreadPoolExecutor
for scenario in ['same-driver','same-connector']:
 a=Client('a');ua=a.register();a.fund();b=a
 if scenario=='same-connector':b=Client('b');ub=b.register();b.fund()
 sta,ka=a.pick();kb=ka
 if scenario=='same-driver':
  kb=next(k for s in a.call('GET','/api/v1/stations') if s['isSimulated'] for k in s['connectors'] if k['powerType']=='DC' and k['status']=='AVAILABLE' and k['evseUid']!=ka['evseUid'])
 qa=a.quote(ka);qb=b.quote(kb);barrier=threading.Barrier(2)
 def start(args):
  client,k,q=args;barrier.wait();return client,client.start(k,q)
 note('CONCURRENT SCENARIO: '+scenario)
 with ThreadPoolExecutor(2) as pool: outcomes=list(pool.map(start,[(a,ka,qa),(b,kb,qb)]))
 a.call('GET','/api/v1/wallet');b.call('GET','/api/v1/wallet')
 for client,s in outcomes:
  if s.get('id'):accounting(s['id']);client.positive(s);client.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])
 a.call('GET','/api/v1/wallet');b.call('GET','/api/v1/wallet')

 sql("SELECT s.user_id,count(DISTINCT s.id) AS sessions,count(DISTINCT r.session_id) AS reservations,count(DISTINCT c.id) AS cdrs FROM charging_sessions s LEFT JOIN wallet_reservations r ON r.session_id=s.id LEFT JOIN cdrs c ON c.session_id=s.id WHERE s.user_id IN ('"+ua['user']['id']+"','"+(ub['user']['id'] if scenario=='same-connector' else ua['user']['id'])+"') GROUP BY s.user_id;")
