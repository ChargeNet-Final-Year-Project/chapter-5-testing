from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client();c.register();c.fund()
def vehicle(name,kind,default=False):return dict(name=name,licensePlate='CH5 1',connectorType=kind,batteryCapacity=60,isDefault=default)
a=c.call('POST','/api/v1/vehicles',vehicle('Type 2','TYPE2')); b=c.call('POST','/api/v1/vehicles',vehicle('CCS2','CCS2'))
c.call('PUT','/api/v1/vehicles/'+a['id'],vehicle('Edited Type 2','TYPE2',True)); c.call('GET','/api/v1/vehicles')
s,k=c.pick();q=c.quote(k);c.start(k,q)
c.call('PUT','/api/v1/vehicles/'+b['id'],vehicle('Default CCS2','CCS2',True));s,k=c.pick(power='AC');q=c.quote(k);live=c.start(k,q)
if live.get('id'):c.positive(live);c.call('POST','/api/v1/sessions/'+live['id']+'/stop');accounting(live['id'])
c.call('DELETE','/api/v1/vehicles/'+a['id']);c.call('GET','/api/v1/vehicles')
