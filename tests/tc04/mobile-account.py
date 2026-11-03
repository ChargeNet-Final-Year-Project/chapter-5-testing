from mobile import *
adb('shell','am','force-stop','com.chargenet.mobile');launch();time.sleep(12);tap(900,2250);shot('restored-profile');tap(540,1615);time.sleep(2);shot('signed-out-login');tap(540,1350);shot('registration-form')
