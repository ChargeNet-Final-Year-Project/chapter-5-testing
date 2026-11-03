from mobile import *
from restart import restart
from proxy import start_proxy,state
restart(18081);proxy=start_proxy();c=Client()
try:
 c.login();c.fund();station,k=c.pick();q=c.quote(k);s=c.start(k,q);c.positive(s)
 adb('shell','am','force-stop','com.chargenet.mobile');launch();time.sleep(12);tap(540,2130);time.sleep(3);shot('live-before-loss');c.call('GET','/api/v1/sessions/'+s['id'])
 state['drop_sse']=True;time.sleep(14);shot('sse-only-interruption-rest-available');c.call('GET','/api/v1/sessions/'+s['id'])
 state['drop_sse']=False;state['replay_old']=True;note('Replay is armed for the next SSE connection after a newer REST snapshot.')
 try:
  adb('shell','svc','data','disable');adb('shell','svc','wifi','disable');time.sleep(20);shot('all-connectivity-lost');c.call('GET','/api/v1/sessions/'+s['id'])
 finally:
  adb('shell','svc','data','enable');adb('shell','svc','wifi','enable')
 time.sleep(9);shot('network-restored-before-explicit-retry');tap(230,505);time.sleep(6);shot('connectivity-restored');shot('after-old-frame-replay');c.call('GET','/api/v1/sessions/'+s['id']);c.call('POST','/api/v1/sessions/'+s['id']+'/stop');time.sleep(2);shot('confirmed-completion-after-recovery');accounting(s['id'])
finally:
 state['drop_sse']=False;adb('shell','svc','data','enable');adb('shell','svc','wifi','enable');proxy.shutdown();proxy.server_close();restart(18080)
