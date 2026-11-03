from partner import *
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
    approve(admin,identity)
    Client('discovery').call('GET','/ocpi/emsp/versions',headers=auth(token_c));Client('discovery').call('GET','/ocpi/emsp/2.3.0',headers=auth(token_c))
    Client('replay').call('POST','/ocpi/emsp/2.3.0/credentials',payload,auth(token_a))
    payload['token']='rotated-'+uuid.uuid4().hex
    rotated=Client('rotation').call('PUT','/ocpi/emsp/2.3.0/credentials',payload,auth(token_c));new_token=rotated['data']['token']
    Client('old').call('GET','/ocpi/emsp/2.3.0/credentials',headers=auth(token_c));Client('new').call('GET','/ocpi/emsp/2.3.0/credentials',headers=auth(new_token));Client('delete').call('DELETE','/ocpi/emsp/2.3.0/credentials',headers=auth(new_token));operator.call('GET','/admin/api/cpo')
finally:
    server.shutdown()
