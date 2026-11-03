from restart import *
c=Client();c.register();c.fund();station,k=c.pick();q=c.quote(k);s=c.start(k,q);before=c.positive(s);accounting(s['id'])
note('Disposable crash fixture: persist the same settlement intent fields as Store.RequestSettlement before abruptly killing the backend.')
sql("UPDATE charging_sessions SET settlement_requested_status='COMPLETED',settlement_requested_reason='USER' WHERE id='"+s['id']+"';")
sql("SELECT id,status,kwh_delivered,original_cost,exchange_rate,settlement_requested_status,settlement_requested_reason FROM charging_sessions WHERE id='"+s['id']+"';")
restart()
for _ in range(30):
 row=c.call('GET','/api/v1/sessions/'+s['id'])
 if row.get('cdrId'):break
 time.sleep(1)
accounting(s['id']);c.call('GET','/api/v1/wallet/transactions');restart();c.call('GET','/api/v1/sessions/'+s['id']);accounting(s['id']);c.call('GET','/api/v1/wallet/transactions')
