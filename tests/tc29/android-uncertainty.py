from mobile import *
import base64
c=Client();c.login();c.fund();station,k=c.pick();q=c.quote(k);s=c.start(k,q);live=c.positive(s)
adb('shell','am','force-stop','com.chargenet.mobile');launch();time.sleep(12);tap(540,2130);time.sleep(2);shot('live-before-unconfirmed-stop')
control=Client('control')
try:
 control.call('POST','/emulator/voltgo/ocpi/admin/scenario',dict(offline=True))
 tap(540,2225);shot('stop-confirmation-input');tap(670,1430);time.sleep(2);shot('unconfirmed-stop-remains-active');accounting(s['id'])
 for i in range(2):
  c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])
finally:control.call('POST','/emulator/voltgo/ocpi/admin/scenario',dict(offline=False))
live=c.call('GET','/api/v1/sessions/'+s['id']);partner=sql("SELECT party_id,token_c,token_b FROM cpo_partners WHERE id='cpo_voltgo';")[0];remote=sql("SELECT coalesce(ocpi_session_id,id) AS remote FROM charging_sessions WHERE id='"+s['id']+"';")[0]['remote']
headers={'Authorization':'Token '+base64.b64encode(partner['token_c'].encode()).decode()}
terminal=dict(country_code='MY',party_id=partner['party_id'],id=remote,start_date_time=s['startTime'],end_date_time=datetime.datetime.now(datetime.timezone.utc).isoformat(),kwh=live['kwhDelivered'],status='COMPLETED',authorization_reference=s['id'])
Client('authoritative').call('PUT','/ocpi/emsp/2.3.0/sessions/MY/'+partner['party_id']+'/'+remote,terminal,headers);time.sleep(1)
accounting(s['id'])
for i in range(2):c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])

shot('authoritative-completion-receipt');tap(790,2225)

Client('operator-cleanup').call('POST','/emulator/voltgo/ocpi/2.3.0/commands/STOP_SESSION',dict(session_id=remote,response_url=BASE+'/ocpi/emsp/2.3.0/commands/STOP_SESSION/'+s['id']),{'Authorization':'Token '+base64.b64encode(partner['token_b'].encode()).decode()});time.sleep(1);accounting(s['id'])
