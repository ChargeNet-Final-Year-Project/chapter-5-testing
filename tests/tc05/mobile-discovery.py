from mobile import *
launch()
for operator,query in [('voltgo','Batu Kawan'),('chargesync','Marina Bay'),('ecowatt','Hat Yai East')]:
 tap(840,160);fill(450,160,query);time.sleep(1);shot(operator+'-search-input-and-results');tap(450,325);time.sleep(1);adb('shell','input','swipe','700','1970','700','1100','600');time.sleep(1);shot(operator+'-station-and-connectors')
