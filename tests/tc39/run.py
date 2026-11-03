from capture import *
from ui import *
import base64,hashlib,hmac
c=Client('throttle')
for i in range(8):c.call('POST','/admin/api/login',dict(email='throttle-'+HERE.name+'@example.test',password='wrong-password'))
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);ctx=b.new_context(viewport={'width':1440,'height':1000},timezone_id='Asia/Kuala_Lumpur');page=ctx.new_page();login(page)
 cookie=next(x for x in ctx.cookies() if x['name']=='cn_portal');head,payload,_=cookie['value'].split('.')
 claims=json.loads(base64.urlsafe_b64decode(payload+'='*((-len(payload))%4)));claims['iat']=int(time.time())-3600;claims['exp']=int(time.time())-60
 encoded=base64.urlsafe_b64encode(json.dumps(claims,separators=(',',':')).encode()).decode().rstrip('=');signing=head+'.'+encoded;signature=base64.urlsafe_b64encode(hmac.new(b'chapter-five-disposable-local-secret',signing.encode(),hashlib.sha256).digest()).decode().rstrip('=')
 note('Expired JWT claims sent to browser: '+json.dumps(claims));ctx.add_cookies([{**cookie,'value':signing+'.'+signature}]);page.goto('http://localhost:15173/#/ledger');page.reload();page.wait_for_timeout(1000);shot(page,'expired-session-rejected')
 ctx.clear_cookies();login(page);page.get_by_role('button',name='Sign out',exact=True).click();page.wait_for_timeout(700);page.goto('http://localhost:15173/#/network');page.wait_for_timeout(700);shot(page,'signed-out-protected-navigation')
 b.close()
