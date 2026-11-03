from partner import *
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
    approve(admin,identity);driver.call('GET','/api/v1/stations?cpoId='+identity)
    state['status']='OUTOFORDER';state['price']=1.75;clock=time.perf_counter()
    Client('push').call('PUT','/ocpi/emsp/2.3.0/tariffs/MY/'+PARTY+'/price-'+PARTY,tariff(),auth(token_c));Client('push').call('PUT','/ocpi/emsp/2.3.0/locations/MY/'+PARTY+'/LOCAL01',location(),auth(token_c))
    driver.call('GET','/api/v1/stations?cpoId='+identity);operator.call('GET','/admin/api/network');note('Push to API visibility milliseconds: '+str((time.perf_counter()-clock)*1000))
    sql("SELECT s.cpo_id,s.name,k.status,k.tariff_per_kwh FROM stations s JOIN connectors k ON k.station_id=s.id WHERE s.cpo_id='"+identity+"';")
    state.update(status='AVAILABLE',price=1.25);Client('restore').call('PUT','/ocpi/emsp/2.3.0/tariffs/MY/'+PARTY+'/price-'+PARTY,tariff(),auth(token_c));Client('restore').call('PUT','/ocpi/emsp/2.3.0/locations/MY/'+PARTY+'/LOCAL01',location(),auth(token_c))
finally:
    server.shutdown()
