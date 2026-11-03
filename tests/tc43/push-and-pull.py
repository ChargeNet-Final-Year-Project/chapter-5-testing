from partner import *
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
 approve(admin,identity);driver.call('GET','/api/v1/stations?cpoId='+identity)
 note('TC43 controlled-source timing: normal 300-second scheduler, one additional isolated station. No push and no direct sync call for this change.')
 state.update(name='TC43 Scheduled Recovery',price=1.75);started=time.perf_counter()
 for i in range(65):
  latest=driver.call('GET','/api/v1/stations?cpoId='+identity);elapsed=time.perf_counter()-started;note('Pull observation elapsed seconds: '+str(elapsed))
  if latest and latest[0]['name']==state['name'] and latest[0]['connectors'][0]['tariffPerKwh']==1.75:break
  time.sleep(5)
 note('Scheduled-pull observed delay seconds: '+str(elapsed));operator.call('GET','/admin/api/network')
 state.update(status='OUTOFORDER',price=1.85);clock=time.perf_counter();Client('push').call('PUT','/ocpi/emsp/2.3.0/tariffs/MY/'+PARTY+'/price-'+PARTY,tariff(),auth(token_c));Client('push').call('PUT','/ocpi/emsp/2.3.0/locations/MY/'+PARTY+'/LOCAL01',location(),auth(token_c));driver.call('GET','/api/v1/stations?cpoId='+identity);note('Push-to-API visibility milliseconds: '+str((time.perf_counter()-clock)*1000))
finally:
 admin.call('PUT','/admin/api/admin/cpos/'+identity+'/status',dict(status='SUSPENDED'));server.shutdown()
