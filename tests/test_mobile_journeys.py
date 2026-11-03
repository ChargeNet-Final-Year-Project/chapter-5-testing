import sys,time
import android_controls as m
from test_api_and_accounting import Client,save

operator=sys.argv[1]
c=Client();login=c.login();before=c.call('GET','/api/v1/wallet')[1]
m.swipe(700,1970,700,1200)
m.shot('TC05_'+operator+'_connectors','TC05;TC09')
m.click_last('Start charging')
m.shot('TC09_'+operator+'_estimate','TC09;TC34')
m.click('Start charging with confirmation');m.click_last('Start charging');time.sleep(2)
code,s,_=c.call('GET','/api/v1/sessions/active');assert code==200 and s.get('id'),s
session_id=s['id']
m.shot('TC09_'+operator+'_live','TC09',session_id)
m.click('Stop charging with confirmation');m.click_last('Stop charging');time.sleep(1)
m.shot('TC11_'+operator+'_receipt','TC09;TC11',session_id)
_,receipt,_=c.call('GET','/api/v1/sessions/'+session_id)
after=c.call('GET','/api/v1/wallet')[1]
assert receipt['status']=='COMPLETED' and receipt['cdrId'] and receipt['kwhDelivered']>0
assert round(before['balance']-after['balance'],2)==receipt['totalCost'] and after['reserved']==0
save('evidence/integration/TC09_mobile_'+operator+'_journey.json',dict(driver_id=login['user']['id'],captured_at=m.now(),session_id=session_id,live=s,receipt=receipt,walletBefore=before,walletAfter=after))
m.click('Receipt details',partial=True);m.shot('TC11_'+operator+'_receipt_details','TC11;TC34',session_id);m.click('Copy receipt');m.click('Done')
print('Completed mobile journey',operator,session_id,flush=True)
