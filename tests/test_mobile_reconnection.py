import time
import android_controls as m
from test_api_and_accounting import Client,save

c=Client();user=c.login()['user']['id']
m.click('Home',partial=True)
if not any(n.get('content-desc')=='Start charging' or n.get('text')=='Start charging' for n in m.nodes()):m.swipe(700,1970,700,1200)
m.click_last('Start charging');m.click('Start charging with confirmation');m.click_last('Start charging');time.sleep(2)
session=c.call('GET','/api/v1/sessions/active')[1];sid=session['id']
m.shot('TC30_before_complete_network_loss','TC30',sid)
try:
    m.adb('shell','svc','data','disable');m.adb('shell','svc','wifi','disable')
    time.sleep(14)
    labels=[n.get('content-desc') or n.get('text') for n in m.nodes()]
    if not any('Updates interrupted' in x for x in labels if x):
        time.sleep(16);labels=[n.get('content-desc') or n.get('text') for n in m.nodes()]
    m.shot('TC30_complete_network_loss','TC30',sid)
    interrupted=any('Updates interrupted' in x for x in labels if x)
    save('evidence/reliability/tc30-telemetry-recovery/android.json',dict(at=m.now(),session_id=sid,user_id=user,wifi=False,mobile_data=False,labels=labels,interruption_feedback_visible=interrupted,terminal_receipt_visible=any('Charging complete' in x for x in labels if x)))
finally:
    m.adb('shell','svc','data','enable');m.adb('shell','svc','wifi','enable')
time.sleep(6)
labels=[n.get('content-desc') or n.get('text') or '' for n in m.nodes()]
manual_retry=any('Updates interrupted' in label for label in labels)
if manual_retry:
    m.click('Retry live updates')
deadline=time.monotonic()+30
while time.monotonic()<deadline:
    labels=[n.get('content-desc') or n.get('text') or '' for n in m.nodes()]
    after=c.call('GET','/api/v1/sessions/active')[1]
    assert after['id']==sid
    if not any('Updates interrupted' in label for label in labels) and after['kwhDelivered']>session['kwhDelivered']:
        break
    time.sleep(1)
else:
    raise AssertionError('Fresh readings did not resume on the same session')
m.shot('TC30_complete_network_restored','TC30',sid)
m.click('Stop charging with confirmation');m.click_last('Stop charging');time.sleep(1)
final=c.call('GET','/api/v1/sessions/'+sid)[1]
save('evidence/reliability/tc30-telemetry-recovery/android-confirmed-ui-recovery.json',dict(at=m.now(),session_id=sid,restored=after,final=final,manual_retry_used=manual_retry,interruption_feedback_visible_after_retry=False))
m.click('Done')
assert interrupted,'full network-loss feedback was not observed'
print('Observed uncertainty and same-session recovery',sid)
