from partner import *
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
    approve(admin,identity);before=driver.call('GET','/api/v1/stations?cpoId='+identity)
    client=Client('invalid')
    client.call('PUT','/ocpi/emsp/2.3.0/locations/MY/'+PARTY+'/LOCAL01',{'broken':'payload'},auth(token_c))
    driver.call('GET','/api/v1/stations/stn_demo_batu_kawan')
    foreign=location();foreign['party_id']='VLT';foreign['id']='DEMO-BATU-KAWAN';client.call('PUT','/ocpi/emsp/2.3.0/locations/MY/VLT/DEMO-BATU-KAWAN',foreign,auth(token_c))
    driver.call('GET','/api/v1/stations/stn_demo_batu_kawan')
    wrong=location();wrong['id']='CONTRADICTORY';client.call('PUT','/ocpi/emsp/2.3.0/locations/MY/'+PARTY+'/LOCAL01',wrong,auth(token_c))
    bad=tariff();bad['currency']='USD';client.call('PUT','/ocpi/emsp/2.3.0/tariffs/MY/'+PARTY+'/price-'+PARTY,bad,auth(token_c))
    driver.call('GET','/api/v1/stations?cpoId='+identity);operator.call('GET','/admin/api/network')
finally:
    server.shutdown()
