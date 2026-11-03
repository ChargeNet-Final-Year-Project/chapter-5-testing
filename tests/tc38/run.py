from partner import *
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
 for header in [{},{'Authorization':'Token unknown'},auth('unknown')]:
  for path in ['/ocpi/emsp/versions','/ocpi/emsp/2.3.0/credentials','/ocpi/emsp/2.3.0/locations']:
   Client('invalid').call('GET',path,headers=header)
 Client('reused-a').call('POST','/ocpi/emsp/2.3.0/credentials',payload,auth(token_a))
 approve(admin,identity);driver.call('GET','/api/v1/stations?cpoId='+identity)
 Client('mismatch').call('PUT','/ocpi/emsp/2.3.0/locations/MY/BAD/LOCAL01',location(),auth(token_c))
 Client('callback').call('POST','/ocpi/emsp/2.3.0/commands/STOP_SESSION/unknown-command',dict(result='ACCEPTED'),auth(token_a))
 driver.call('GET','/api/v1/stations?cpoId='+identity);operator.call('GET','/admin/api/cpo')
finally:server.shutdown()
