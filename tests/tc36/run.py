from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
a=Client('owner');owner=a.register();a.fund();v=a.call('POST','/api/v1/vehicles',dict(name='Private',licensePlate='OWN 1',connectorType='CCS2',batteryCapacity=60,isDefault=True));st,k=a.pick();q=a.quote(k);s=a.start(k,q);a.positive(s)
b=Client('other');b.register();b.fund();accounting(s['id'])
for method,path,body in [('PUT','/api/v1/vehicles/'+v['id'],dict(name='Intrusion',licensePlate='BAD 1',connectorType='CCS2',batteryCapacity=60,isDefault=True)),('DELETE','/api/v1/vehicles/'+v['id'],None),('GET','/api/v1/sessions/'+s['id'],None),('GET','/api/v1/sessions/'+s['id']+'/stream',None),('POST','/api/v1/sessions/'+s['id']+'/stop',None),('POST','/api/v1/sessions/start',dict(evseUid=k['evseUid'],quoteId=q['id'],targetSoc=100))]:b.call(method,path,body)
b.call('GET','/api/v1/sessions/history');a.call('GET','/api/v1/vehicles');accounting(s['id']);a.call('POST','/api/v1/sessions/'+s['id']+'/stop')

# Repeat a foreign estimate against its now-available connector, so connector state cannot mask ownership validation.
b.call('POST','/api/v1/sessions/start',dict(evseUid=k['evseUid'],quoteId=q['id'],targetSoc=100));accounting(s['id'])
