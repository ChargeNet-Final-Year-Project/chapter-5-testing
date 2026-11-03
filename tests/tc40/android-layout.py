from mobile import *

def restore():
 adb('shell','wm','size','reset');adb('shell','wm','density','420');adb('shell','settings','put','system','font_scale','1.0');time.sleep(2)

def layouts(screen):
 try:
  for size,scale in [('960x1920','1.0'),('960x1920','2.0'),('1920x960','1.0'),('1920x960','2.0')]:
   adb('shell','wm','size',size);adb('shell','wm','density','480');adb('shell','settings','put','system','font_scale',scale);time.sleep(3);shot(screen+'-'+size+'-scale-'+scale)
   w,h=map(int,size.split('x'));adb('shell','input','swipe',int(w*.8),int(h*.8),int(w*.8),int(h*.3),600);time.sleep(2);shot(screen+'-'+size+'-scale-'+scale+'-scrolled')
 finally:restore()

restore();adb('shell','am','force-stop','com.chargenet.mobile');launch();time.sleep(12);tap(180,2250);layouts('discovery');tap(900,2250);layouts('profile');tap(180,2250)
tap(840,160);fill(450,160,'Batu Kawan');time.sleep(2);tap(450,325);time.sleep(2);adb('shell','input','swipe','700','1970','700','1100','600');time.sleep(2);tap(540,1555);time.sleep(2);layouts('estimate')
# Display settings are restored after every layout group.
