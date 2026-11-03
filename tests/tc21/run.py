from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client();c.register();c.fund(500)
for cpo in ['cpo_voltgo','cpo_chargesync','cpo_ecowatt']:
 for country in ['MY','SG','TH']:
  station,k=c.pick(country,cpo);q=c.quote(k);c.call('GET','/api/v1/wallet');s=c.start(k,q);c.positive(s);c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])
