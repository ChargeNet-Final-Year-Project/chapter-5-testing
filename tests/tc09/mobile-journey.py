from mobile import *
import sys
queries=sys.argv[1:] or ['Batu Kawan','Marina Bay','Hat Yai East']
c=Client();c.login();c.call('GET','/api/v1/auth/me')
for query in queries:
 tap(180,2250);tap(840,160);fill(450,160,query);time.sleep(1);shot(query+'-search');tap(450,325);time.sleep(1.5);adb('shell','input','swipe','700','1970','700','1100','600');time.sleep(1);shot(query+'-connectors');tap(540,1555);time.sleep(1);shot(query+'-estimate');before=c.call('GET','/api/v1/wallet')
 adb('shell','input','swipe','700','1900','700','1400','500');tap(540,2150);shot(query+'-confirmation-dialog');tap(730,1430);time.sleep(4);shot(query+'-live');s=c.call('GET','/api/v1/sessions/active')
 if not isinstance(s,dict) or not s.get('id'):raise RuntimeError('No active session after UI confirmation; inspect screenshots')
 tap(540,2225);shot(query+'-stop-confirmation');tap(670,1430);time.sleep(3);shot(query+'-receipt');c.call('GET','/api/v1/sessions/'+s['id']);c.call('GET','/api/v1/wallet');c.call('GET','/api/v1/wallet/transactions');accounting(s['id']);tap(790,2225);time.sleep(1)
