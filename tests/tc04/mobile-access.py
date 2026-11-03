from mobile import *
note('Start from a clean test app, complete its two onboarding pages, then exercise login.')
adb('shell','pm','clear','com.chargenet.mobile');adb('shell','pm','grant','com.chargenet.mobile','android.permission.ACCESS_FINE_LOCATION');adb('shell','pm','grant','com.chargenet.mobile','android.permission.ACCESS_COARSE_LOCATION');launch();time.sleep(12);tap(540,1550);tap(540,1590);time.sleep(2)
fill(500,580,'demo@chargenet.my');fill(500,780,'WrongPassword123');shot('invalid-login-input');tap(500,975);time.sleep(2);shot('invalid-login-result')
note('Tap the Use demo account shortcut in the error-expanded form; it clears the error and restores the normal form.')
tap(540,1266);shot('valid-login-input');tap(540,975);time.sleep(6);shot('valid-login-result')
