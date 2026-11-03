from mobile import *
from restart import restart
from delay_proxy import start_proxy
restart(18081);proxy=start_proxy()
adb('shell','am','force-stop','com.chargenet.mobile');launch();time.sleep(12)
try:
 c=Client();c.login();tap(180,2250);tap(840,160);fill(450,160,'Batu Kawan');tap(450,325);time.sleep(1.5);adb('shell','input','swipe','700','1970','700','1100','600');time.sleep(2);tap(540,1555);adb('shell','input','swipe','700','1900','700','1400','500');time.sleep(1);shot('estimate-light-theme');c.call('GET','/api/v1/sessions/active');c.call('GET','/api/v1/wallet')
 adb('shell','input','swipe','120','2120','350','2120','600');shot('cancelled-short-drag');c.call('GET','/api/v1/sessions/active');c.call('GET','/api/v1/wallet')
 tap(540,2260);shot('accessible-confirmation-dialog');tap(730,1430);tap(730,1430);shot('busy-controls-during-real-start');time.sleep(4);shot('one-live-session');s=c.call('GET','/api/v1/sessions/active');accounting(s['id']);tap(540,2225);tap(670,1430);time.sleep(2);shot('receipt-light-theme');accounting(s['id']);tap(790,2225)
finally:
 proxy.shutdown();proxy.server_close();restart(18080)
