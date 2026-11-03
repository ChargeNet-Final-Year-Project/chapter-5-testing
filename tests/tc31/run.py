from restart import *
c=Client();c.register();c.fund();station,k=c.pick();q=c.quote(k);s=c.start(k,q);before=c.positive(s);accounting(s['id'])
restart()
for _ in range(30):
 row=c.call('GET','/api/v1/sessions/'+s['id'])
 if row.get('cdrId'):break
 time.sleep(1)
if row.get('status') in ['PENDING','CHARGING']:
 c.positive(row);c.call('POST','/api/v1/sessions/'+s['id']+'/stop')
accounting(s['id']);c.call('GET','/api/v1/wallet/transactions')
