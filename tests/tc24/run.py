from capture import *
import base64
c=Client();c.register();c.fund();station,k=c.pick();q=c.quote(k);s=c.start(k,q);live=c.positive(s)
partner=sql("SELECT party_id,token_c FROM cpo_partners WHERE id='cpo_voltgo';")[0]
foreign=sql("SELECT party_id,token_c FROM cpo_partners WHERE id='cpo_chargesync';")[0]
auth=lambda token:{'Authorization':'Token '+base64.b64encode(token.encode()).decode()}
remote=sql("SELECT coalesce(ocpi_session_id,id) AS remote FROM charging_sessions WHERE id='"+s['id']+"';")[0]['remote']
Client('callback').call('POST','/ocpi/emsp/2.3.0/commands/START_SESSION/'+s['id'],dict(result='ACCEPTED'),auth(partner['token_c']))
Client('foreign-callback').call('POST','/ocpi/emsp/2.3.0/commands/START_SESSION/'+s['id'],dict(result='ACCEPTED'),auth(foreign['token_c']))
body=dict(country_code='MY',party_id=partner['party_id'],id=remote,start_date_time=s['startTime'],kwh=live['kwhDelivered'],status='ACTIVE',authorization_reference=s['id'])
Client('receiver').call('PUT','/ocpi/emsp/2.3.0/sessions/MY/'+partner['party_id']+'/'+remote,body,auth(partner['token_c']));c.call('GET','/api/v1/sessions/'+s['id']);accounting(s['id'])
Client('foreign').call('PUT','/ocpi/emsp/2.3.0/sessions/MY/'+partner['party_id']+'/'+remote,body,auth(foreign['token_c']));accounting(s['id'])
cdr=dict(country_code='MY',party_id=partner['party_id'],id='cdr-source-'+uuid.uuid4().hex,session_id=remote,start_date_time=s['startTime'],end_date_time=datetime.datetime.now(datetime.timezone.utc).isoformat(),currency=q['originalCurrency'],total_energy=live['kwhDelivered'],total_time=.01,total_cost=dict(excl_vat=999),cpo_note='Controlled duplicate receiver experiment')
for i in range(2):
 Client('cdr').call('POST','/ocpi/emsp/2.3.0/cdrs',cdr,auth(partner['token_c']));time.sleep(.5);accounting(s['id']);c.call('GET','/api/v1/wallet/transactions')
