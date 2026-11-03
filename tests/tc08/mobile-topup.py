from mobile import *
c=Client();c.login();c.call('GET','/api/v1/wallet');c.call('GET','/api/v1/wallet/transactions');tap(900,2250);tap(230,730);tap(635,1375);shot('topup-100-input');tap(540,2280);time.sleep(2);shot('topup-result');c.call('GET','/api/v1/wallet');c.call('GET','/api/v1/wallet/transactions')
