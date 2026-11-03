from mobile import *
adb('shell','wm','size','960x1920');adb('shell','wm','density','480');adb('shell','settings','put','system','font_scale','2.0');time.sleep(3)
for _ in range(6):adb('shell','input','swipe','900','500','900','1600','500')
time.sleep(2);shot('estimate-200-top')
for _ in range(8):adb('shell','input','swipe','900','1600','900','500','500')
time.sleep(2);shot('estimate-200-bottom')
