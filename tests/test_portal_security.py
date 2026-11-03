import os
import base64,hashlib,hmac,json,sys,time
from test_support import ROOT,RUN,now
from test_api_and_accounting import Client,save,sql
from playwright.sync_api import sync_playwright

def run():
    results=[]
    with sync_playwright() as p:
        b=p.chromium.launch(channel='msedge',headless=True);ctx=b.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'],timezone_id='Asia/Kuala_Lumpur');page=ctx.new_page()
        def login(email,password):
            ctx.clear_cookies();page.goto('http://localhost:15173/#/login');page.reload();page.wait_for_timeout(400)
            page.locator('[name=email]').fill(email);page.locator('[name=password]').fill(password);page.get_by_role('button',name='Sign in',exact=True).click();page.wait_for_timeout(700)
        def shot(name,case):
            stamp=now();dest=RUN/'evidence/captures'/('edge_'+stamp.replace(':','').replace('+','_')+'_'+name+'.png');page.screenshot(path=str(dest))
            with (RUN/'provenance/captures.events.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(dict(path=dest.relative_to(RUN).as_posix(),captured_at=stamp,case_id=case,platform='Microsoft Edge Chromium',session_id=''))+'\n')
            return dest.relative_to(RUN).as_posix()
        login('admin@chargenet.my',os.environ.get('CHARGENET_ADMIN_PASSWORD', ''))
        for width in [1440,390]:
            page.set_viewport_size({'width':width,'height':1000});page.goto('http://localhost:15173/#/admin');page.wait_for_timeout(600)
            page.keyboard.press('Tab');metrics=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,focus:document.activeElement.tagName})');assert metrics['scroll']<=width
            results.append(dict(case_id='TC42',scope='administrator navigation',metrics=metrics,capture=shot(f'TC42_admin_{width}','TC42;TC12'),status='Pass'))
        page.set_viewport_size({'width':1440,'height':1000})
        login('ops@voltgo.my',os.environ.get('CHARGENET_OPERATOR_PASSWORD', ''));page.goto('http://localhost:15173/#/ledger');page.wait_for_timeout(500)
        for currency in ['MYR','SGD','THB']:
            page.get_by_label('From',exact=True).fill('2026-10-26');page.get_by_label('To',exact=True).fill('2026-10-26');page.get_by_label('Revenue currency',exact=True).select_option(currency);page.wait_for_timeout(400)
            assert '26' in page.locator('body').inner_text()
            with page.expect_download() as d:page.get_by_role('button',name='Export CSV',exact=True).click()
            dest=RUN/f'evidence/integration/TC15_browser_full_fixture_{currency}.csv';d.value.save_as(str(dest))
            results.append(dict(case_id='TC15',currency=currency,capture=shot('TC15_full_range_'+currency,'TC15;TC37'),status='Pass'))
        # Correctly signed JWT, same claims, expiration in the past. Do not log it.
        cookie=next(x for x in ctx.cookies() if x['name']=='cn_portal');head,payload,_=cookie['value'].split('.')
        dec=lambda value:json.loads(base64.urlsafe_b64decode(value+'='*((-len(value))%4)))
        enc=lambda value:base64.urlsafe_b64encode(json.dumps(value,separators=(',',':')).encode()).decode().rstrip('=')
        claims=dec(payload);claims['iat']=int(time.time())-3600;claims['exp']=int(time.time())-60
        signing=head+'.'+enc(claims);signature=base64.urlsafe_b64encode(hmac.new(os.environ.get('CHARGENET_JWT_SECRET', '').encode(),signing.encode(),hashlib.sha256).digest()).decode().rstrip('=')
        ctx.add_cookies([{**cookie,'value':signing+'.'+signature}]);page.reload();page.wait_for_timeout(700)
        assert page.get_by_role('heading',name='Sign in',exact=True).is_visible()
        results.append(dict(case_id='TC39',scope='correctly signed expired JWT',status='Pass',expired_by_seconds=60,protected_view_removed=True))
        save('evidence/portal/Browser partial.json',results)
        # Unused Token A reveal and clipboard interaction on a new pending CPO.
        c=Client();code,new,_=c.call('POST','/admin/api/register',dict(companyName='Petir Protocol Lab',partyId='PFX',countryCode='MY',contactEmail='token-ui@example.test',contactName='Synthetic Token Operator',password=os.environ.get('CHARGENET_FIXTURE_PASSWORD', ''),bank=dict(bankName='Synthetic Bank',accountHolder='Synthetic',accountNo=os.environ.get('CHARGENET_FIXTURE_BANK_ACCOUNT', '')),payoutCycle='MONTHLY'))
        if code!=201:
            assert c.call('POST','/admin/api/login',dict(email='token-ui@example.test',password=os.environ.get('CHARGENET_FIXTURE_PASSWORD', '')))[0]==200
            new={'cpo':c.call('GET','/admin/api/cpo')[1]}
        token=new['cpo']['tokenA'];login('token-ui@example.test',os.environ.get('CHARGENET_FIXTURE_PASSWORD', ''));page.goto('http://localhost:15173/#/credentials');page.wait_for_timeout(500)
        page.get_by_role('button',name='Reveal',exact=True).click();assert token in page.locator('body').inner_text()
        page.locator('.field').filter(has_text='Token A (one-time registration token)').get_by_role('button',name='Copy',exact=True).click();copied=page.evaluate('navigator.clipboard.readText()');assert copied==token
        page.evaluate('navigator.clipboard.writeText("")');page.get_by_role('button',name='Hide',exact=True).click()
        assert token not in page.locator('body').inner_text()
        results.append(dict(case_id='TC13',scope='unused Token A reveal/copy/hide',status='Pass',clipboard_matched=True,capture=shot('TC13_unused_token_masked','TC13')))
        # No unmasked token screenshot or clipboard content is retained.
        b.close()
    save('evidence/portal/test_portal_security.json',results)
    print('Final browser cases',len(results))

if __name__=='__main__':run()
