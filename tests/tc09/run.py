from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client();c.login();c.fund()
for country,cpo in [('MY','cpo_voltgo'),('SG','cpo_chargesync'),('TH','cpo_ecowatt')]:
 c.call('GET','/api/v1/auth/me');c.call('GET','/api/v1/wallet');station,k=c.pick(country,cpo);q=c.quote(k);session=c.start(k,q);c.positive(session);c.call('POST','/api/v1/sessions/'+session['id']+'/stop');c.call('GET','/api/v1/wallet');c.call('GET','/api/v1/wallet/transactions');accounting(session['id'])
