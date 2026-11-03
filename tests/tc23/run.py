from capture import *
c=Client();c.register();c.fund();station,k=c.pick();q=c.quote(k)
a=Client('admin');a.call('POST','/admin/api/login',dict(email='admin@chargenet.my',password='Admin1234!'))
try:
 a.call('POST','/emulator/voltgo/ocpi/admin/scenario',dict(offline=True));c.start(k,q);c.call('GET','/api/v1/wallet')
finally:a.call('POST','/emulator/voltgo/ocpi/admin/scenario',dict(offline=False))
try:
 a.call('PUT','/admin/api/admin/cpos/cpo_voltgo/status',dict(status='SUSPENDED'));c.call('GET','/api/v1/stations?cpoId=cpo_voltgo');c.start(k,q);c.call('GET','/api/v1/wallet')
finally:a.call('PUT','/admin/api/admin/cpos/cpo_voltgo/status',dict(status='ACTIVE'))

# Separately make the partner HTTP endpoint unreachable while testing the other partners.
original=sql("SELECT base_url,module_endpoints::text FROM cpo_partners WHERE id='cpo_voltgo';")[0]
try:
 sql("UPDATE cpo_partners SET base_url='http://127.0.0.1:18999',module_endpoints='{}'::jsonb WHERE id='cpo_voltgo';")
 v=Client('offline-operator');v.call('POST','/admin/api/login',dict(email='ops@voltgo.my',password='Cpo1234!'));v.call('POST','/admin/api/cpo/handshake-test');v.call('GET','/admin/api/cpo')
 for operator in ['chargesync','ecowatt']:
  o=Client(operator);o.call('POST','/admin/api/login',dict(email='ops@'+operator+'.my',password='Cpo1234!'));o.call('POST','/admin/api/cpo/handshake-test');o.call('GET','/admin/api/network')
finally:
 sql("UPDATE cpo_partners SET base_url='"+original['base_url']+"',module_endpoints='"+original['module_endpoints'].replace("'","''")+"'::jsonb WHERE id='cpo_voltgo';")
 v.call('POST','/admin/api/cpo/handshake-test')
