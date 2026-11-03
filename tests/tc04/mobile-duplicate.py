from mobile import *
inputs=json.loads((HERE/'registration-input.json').read_text());tap(540,1640);time.sleep(1);tap(540,1350)
fill(500,640,inputs['name']);fill(500,835,inputs['email']);fill(500,1035,inputs['password']);fill(500,1290,inputs['password']);shot('duplicate-registration-input');tap(500,1800);time.sleep(2);shot('duplicate-registration-result')
adb('shell','input','keyevent','4');time.sleep(1);tap(540,1120);tap(540,975);time.sleep(4);shot('demo-restored-for-next-cases')
