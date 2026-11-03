from mobile import *
c=Client();c.login();tap(900,2250);tap(540,1380);time.sleep(2)
fill(540,335,'Evidence EV');fill(540,540,'CH5 123');fill(540,950,'60');tap(950,1140);shot('vehicle-create-input');tap(540,1335);time.sleep(2);shot('vehicle-created-default');c.call('GET','/api/v1/vehicles')
tap(950,1120);time.sleep(1);fill(540,335,'Evidence EV Edited');fill(540,950,'64');shot('vehicle-edit-input');tap(540,1335);time.sleep(2);shot('vehicle-edited-default');c.call('GET','/api/v1/vehicles');tap(950,1120);time.sleep(1);tap(540,1495);shot('vehicle-delete-confirmation');tap(800,1350);time.sleep(2);shot('vehicle-deleted');c.call('GET','/api/v1/vehicles')
