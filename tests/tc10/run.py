from mobile import *
c=Client();c.login();before=c.call('GET','/api/v1/sessions/active');shot('before-minimise')
adb('shell','input','keyevent','4');time.sleep(1);shot('minimised-monitor');tap(540,2250);shot('activity-during-charge');tap(900,2250);shot('profile-during-charge');adb('shell','input','keyevent','3');time.sleep(2);launch();time.sleep(3);shot('foreground-restored-session');c.call('GET','/api/v1/sessions/active');accounting(before['id'])
