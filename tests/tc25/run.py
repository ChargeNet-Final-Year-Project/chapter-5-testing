from capture import *
c=Client();identity=c.register();c.fund(300);station,k=c.pick();q=c.quote(k)
other=next(con for st in c.call('GET','/api/v1/stations') if st['isSimulated'] for con in st['connectors'] if con['status']=='AVAILABLE' and con['powerType']=='DC' and con['evseUid']!=k['evseUid']);q2=c.quote(other)
note('Disposable eligibility fixture: lower this newly created driver wallet after obtaining its estimate.')
sql("UPDATE wallets SET balance=0 WHERE user_id='"+identity['user']['id']+"';")
c.start(k,q);c.call('GET','/api/v1/wallet');c.fund(300)
c.call('POST','/api/v1/quotes',dict(evseUid='DOES-NOT-EXIST',estimatedKwh='15'));c.call('POST','/api/v1/sessions/start',dict(evseUid='DOES-NOT-EXIST',quoteId=q['id'],targetSoc=100))
try:
 sql("UPDATE connectors SET status='INOPERATIVE' WHERE id='"+k['id']+"';");c.start(k,q);c.call('GET','/api/v1/wallet')
finally:sql("UPDATE connectors SET status='AVAILABLE' WHERE id='"+k['id']+"';")
c.call('POST','/api/v1/vehicles',dict(name='Incompatible fixture',licensePlate='TYPE2 1',connectorType='TYPE2',batteryCapacity=60,isDefault=True));c.start(k,q);c.call('GET','/api/v1/wallet')
c.call('POST','/api/v1/vehicles',dict(name='Compatible fixture',licensePlate='CCS2 1',connectorType='CCS2',batteryCapacity=60,isDefault=True))
s=c.start(k,q)
if s.get('id'):
 c.start(other,q2);accounting(s['id']);c.positive(s);c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])
c.call('GET','/api/v1/wallet')

sql("SELECT count(*) AS sessions,(SELECT count(*) FROM wallet_transactions t JOIN wallets w ON t.wallet_id=w.id WHERE w.user_id='"+identity['user']['id']+"' AND t.type='CHARGING_DEBIT') AS debit_count FROM charging_sessions WHERE user_id='"+identity['user']['id']+"';")
