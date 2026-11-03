from capture import *
for reason,balance,target in [('TARGET_REACHED',100,21),('BALANCE_EXHAUSTED',10,100)]:
 note('SCENARIO '+reason);c=Client(reason);c.register();c.fund(balance);station,k=c.pick();q=c.quote(k)
 s=c.call('POST','/api/v1/sessions/start',dict(evseUid=k['evseUid'],quoteId=q['id'],targetSoc=target),{'Idempotency-Key':uuid.uuid4().hex})
 if not s.get('id'):continue
 for i in range(90):
  row=c.call('GET','/api/v1/sessions/'+s['id'])
  if row.get('cdrId'):break
  time.sleep(1)
 accounting(s['id']);c.call('GET','/api/v1/wallet/transactions');c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])
