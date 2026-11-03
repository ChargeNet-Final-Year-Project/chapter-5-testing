from partner import *
from ui import capture_page
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
    capture_page(email,'credentials','consumed-token-masked')
    operator.call('GET','/admin/api/cpo')
    Client('replay').call('POST','/ocpi/emsp/2.3.0/credentials',payload,auth(token_a))
    approve(admin,identity)
    Client('disconnect').call('DELETE','/ocpi/emsp/2.3.0/credentials',headers=auth(token_c));operator.call('GET','/admin/api/cpo')
    capture_page(email,'credentials','disconnected')
finally:
    server.shutdown()
