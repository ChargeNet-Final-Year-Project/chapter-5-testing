from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client();c.register();c.fund();station,k=c.pick('SG','cpo_chargesync');q=c.quote(k);c.call('GET','/api/v1/wallet');session=c.start(k,q);c.positive(session);c.call('POST','/api/v1/sessions/'+session['id']+'/stop');c.call('GET','/api/v1/sessions/'+session['id']);c.call('GET','/api/v1/sessions/history');c.call('GET','/api/v1/wallet/transactions');accounting(session['id'])
