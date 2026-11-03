from partner import *
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
    approve(admin,identity);driver.call('GET','/api/v1/stations?cpoId='+identity);note('Change SOURCE ONLY; no receiver push and no direct synchronization call. Scheduler remains 300 seconds.')
    state.update(name='Recovered Without Push',price=1.75);started=time.perf_counter()
    for i in range(65):
     latest=driver.call('GET','/api/v1/stations?cpoId='+identity)
     note('Elapsed seconds: '+str(time.perf_counter()-started))
     if latest and latest[0]['name']==state['name'] and latest[0]['connectors'][0]['tariffPerKwh']==1.75:break
     time.sleep(5)
    operator.call('GET','/admin/api/network')
finally:
    server.shutdown()
