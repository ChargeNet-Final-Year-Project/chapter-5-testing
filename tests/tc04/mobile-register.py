from mobile import *
email='ui-driver-'+uuid.uuid4().hex[:8]+'@example.test'
(HERE/'registration-input.json').write_text(json.dumps(dict(name='UI Evidence Driver',email=email,password='LocalOnly123!')),encoding='utf-8')
fill(500,640,'UI Evidence Driver');fill(500,835,email);fill(500,1035,'LocalOnly123!');fill(500,1290,'LocalOnly123!');shot('registration-input');tap(500,1800);time.sleep(4);shot('registration-result');tap(900,2250);shot('registered-profile')
c=Client('new-driver');c.login(email,'LocalOnly123!');c.call('GET','/api/v1/auth/me')
adb('shell','am','force-stop','com.chargenet.mobile');launch();time.sleep(12);tap(900,2250);shot('registered-profile-after-reopen')
