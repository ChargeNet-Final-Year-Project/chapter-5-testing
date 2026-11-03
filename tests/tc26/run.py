from capture import *
import socket
c=Client();identity=c.register();c.fund();station,k=c.pick();q=c.quote(k);key='lost-'+uuid.uuid4().hex
body=dict(evseUid=k['evseUid'],quoteId=q['id'],targetSoc=100);raw=json.dumps(body).encode()
wire=(f'POST /api/v1/sessions/start HTTP/1.1\r\nHost: localhost:18080\r\nContent-Type: application/json\r\nAuthorization: Bearer {c.token}\r\nIdempotency-Key: {key}\r\nContent-Length: {len(raw)}\r\nConnection: close\r\n\r\n').encode()+raw
note('Send complete request through a socket, wait for server commit using SQL, close without reading any response bytes.\n'+wire.decode())
with socket.create_connection(('127.0.0.1',18080),timeout=10) as sock:
 sock.sendall(wire)
 for i in range(60):
  found=sql("SELECT key,response_status,response_body->>'id' AS session_id FROM idempotency_keys WHERE key='"+key+"';")
  if found:break
  time.sleep(.1)
s=c.start(k,q,key);accounting(s['id']);c.positive(s);c.start(k,q,key);accounting(s['id']);c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])

sql("SELECT s.user_id,count(DISTINCT s.id) AS sessions,count(DISTINCT r.session_id) AS reservations,count(DISTINCT c.id) AS cdrs FROM charging_sessions s LEFT JOIN wallet_reservations r ON r.session_id=s.id LEFT JOIN cdrs c ON c.session_id=s.id WHERE s.user_id='"+identity['user']['id']+"' GROUP BY s.user_id;")
