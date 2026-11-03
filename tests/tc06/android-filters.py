from mobile import *
tap(180,2250);tap(840,160);adb('shell','input','keyevent','4');tap(140,315);tap(840,740)
tap(540,1050);tap(540,1175);tap(540,1250);tap(540,1750);shot('malaysia-penang-selected');tap(540,1050);tap(540,1175);shot('country-change-resets-region');tap(540,1050);tap(540,922);tap(540,1250);tap(540,1750)
tap(575,1600);adb('shell','input','swipe','130','1885','232','1885','600');adb('shell','input','swipe','950','1885','437','1885','600');shot('dc-power-range-input');adb('shell','input','swipe','700','2000','700','1200','600');time.sleep(2)
tap(540,1470);tap(540,1690);tap(540,1998);tap(540,2188);shot('combined-filter-final-input');tap(540,2230);time.sleep(2);shot('combined-filter-result')
c=Client();c.login();c.call('GET','/api/v1/stations?country=MY&region=Penang&cpoId=cpo_voltgo&connectorType=CCS2&powerType=DC&minPower=50&maxPower=150')
tap(140,315);tap(840,740);shot('reset-draft-input');tap(985,740);tap(140,315);shot('cancel-preserved-applied-filters');tap(840,740);tap(540,2230);time.sleep(1);shot('reset-applied-result')
fill(450,160,'Batu Kawan');shot('search-result-input');tap(450,325);time.sleep(1.5);shot('search-selection-dismissed-results')
