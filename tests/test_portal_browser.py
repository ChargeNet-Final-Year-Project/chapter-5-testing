import os
import csv
import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_support import ROOT,RUN,now
from test_api_and_accounting import Client,save,sql,scrub

URL='http://localhost:15173/#/'
out=[]
SELECTED=set(sys.argv[1].split(',')) if len(sys.argv)>1 else None
RESULT='evidence/portal/browser-workflow-results.json' if SELECTED else 'evidence/portal/browser-results.json'

def run():
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        ctx=browser.new_context(viewport={'width':1440,'height':1000},locale='en-MY',timezone_id='Asia/Kuala_Lumpur',accept_downloads=True)
        page=ctx.new_page()
        def shot(name,case):
            stamp=now();dest=RUN/'evidence/captures'/('edge_'+stamp.replace(':','').replace('+','_')+'_'+name+'.png')
            page.screenshot(path=str(dest))
            with (RUN/'provenance/captures.events.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(dict(path=dest.relative_to(RUN).as_posix(),captured_at=stamp,case_id=case,session_id='',platform='Microsoft Edge Chromium',viewport=page.viewport_size))+'\n')
            return dest.relative_to(RUN).as_posix()
        def go(route):
            page.goto(URL+route);page.wait_for_timeout(900)
        def step(case,name,fn):
            if SELECTED and case not in SELECTED:return
            started=now()
            try:data=fn();out.append(dict(case_id=case,name=name,status='Pass',started_at=started,finished_at=now(),details=data))
            except Exception as e:out.append(dict(case_id=case,name=name,status='Fail',started_at=started,finished_at=now(),error=str(e)))
            save(RESULT,out)
        def login(email='ops@voltgo.my',password=os.environ.get('CHARGENET_OPERATOR_PASSWORD', '')):
            go('login');page.locator('[name=email]').fill(email);page.locator('[name=password]').fill(password)
            page.get_by_role('button',name='Sign in',exact=True).click();page.wait_for_timeout(1200)
            assert page.locator('h1').first.inner_text()!='Sign in'
        login()
        def basics():
            captures=[]
            for route in ['overview','network','ledger','credentials']:
                go(route);assert page.locator('h1').count()
                captures.append(shot('PF_'+route,'TC13;TC14;TC15;TC42'))
            return {'captures':captures,'browser':browser.version}
        step('TC14','operator navigation',basics)
        def company():
            go('company')
            fields=page.locator('input').evaluate_all('(els)=>els.map(e=>({name:e.name,id:e.id,type:e.type,value:e.type==="password"?"[REDACTED]":e.value}))')
            # Record only field names; banking values remain outside evidence.
            return dict(field_names=[{k:v for k,v in x.items() if k!='value'} for x in fields],heading=page.locator('h1').inner_text())
        step('TC14','company form available',company)
        def ledger():
            go('ledger');results=[]
            for currency in ['MYR','SGD','THB']:
                page.get_by_label('Revenue currency',exact=True).select_option(currency);page.wait_for_timeout(500)
                with page.expect_download() as d:page.get_by_role('button',name='Export CSV',exact=True).click()
                dest=RUN/f'evidence/integration/TC15_browser_export_{currency}.csv';d.value.save_as(str(dest))
                rows=list(csv.reader(dest.open(encoding='utf-8-sig')))
                results.append(dict(currency=currency,file=dest.relative_to(RUN).as_posix(),rows=max(0,len(rows)-2),total_row=rows[-1]))
            page.get_by_label('Revenue currency',exact=True).select_option('MYR');page.wait_for_timeout(300)
            return dict(exports=results,capture=shot('TC15_ledger_export','TC15;TC37'))
        step('TC15','separate-currency browser CSV downloads',ledger)
        def refresh_fault():
            # Network uses the same useResource hook as overview/ledger, and
            # supplies a real 5-second refresh to trigger a failure after load.
            go('network');before=page.locator('h2').all_text_contents();assert before
            page.route('**/admin/api/network',lambda route:route.abort('internetdisconnected'))
            page.wait_for_timeout(5600)
            assert 'Showing last successful data' in page.locator('body').inner_text()
            assert page.locator('h2').all_text_contents()==before
            stale=shot('PF06_stale_network','PF06')
            page.get_by_role('button',name='Retry',exact=True).click();page.wait_for_timeout(500)
            assert 'Showing last successful data' in page.locator('body').inner_text()
            page.unroute('**/admin/api/network')
            page.get_by_role('button',name='Retry',exact=True).click();page.wait_for_timeout(800)
            assert 'Could not refresh network' not in page.locator('body').inner_text()
            return dict(stale_capture=stale,recovered_capture=shot('PF06_recovered_network','PF06'),scope='network screen sharing useResource; overview/ledger not directly refreshed')
        step('PF06','stale data and retry after interrupted request',refresh_fault)
        def layout():
            matrix=[]
            for width in [1440,390]:
                page.set_viewport_size({'width':width,'height':1000})
                for route in ['overview','ledger','network','credentials']:
                    go(route)
                    page.keyboard.press('Tab');active=page.evaluate('document.activeElement?.tagName')
                    metrics=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})')
                    matrix.append(dict(browser='Edge Chromium '+browser.version,viewport_width=width,route=route,keyboard_focus_tag=active,document_width=metrics['scroll'],horizontal_document_overflow=metrics['scroll']>width,capture=shot(f'TC42_{width}_{route}','TC42')))
            page.set_viewport_size({'width':1440,'height':1000})
            with (RUN/'evidence/performance/layout-browser-matrix.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(matrix[0]));w.writeheader();w.writerows(matrix)
            assert not any(x['horizontal_document_overflow'] for x in matrix),matrix
            return matrix
        step('TC42','desktop and narrow keyboard/layout samples',layout)
        def sandbox():
            go('sandbox');assert page.locator('select').count()>=2
            # Choose a bay whose name is explicitly simulated.
            options=page.locator('select').nth(0).locator('option').evaluate_all('(els)=>els.map(e=>({value:e.value,text:e.textContent}))')
            opt=next((x for x in options if 'Butterworth' in x['text'] and 'DC' in x['value'] and 'AVAILABLE' in x['text']),options[0])
            page.locator('select').nth(0).select_option(opt['value']);page.locator('select').nth(1).select_option('START_SESSION')
            before=sql("SELECT currency,count(*) AS count,sum(gross_amount) AS gross FROM cdrs WHERE user_id <> 'usr_sandbox' GROUP BY currency ORDER BY currency;")
            page.get_by_role('button',name='Send command',exact=True).click();page.wait_for_timeout(2300)
            accepted=page.locator('body').inner_text();start=shot('TC16_sandbox_start','TC16')
            page.locator('select').nth(1).select_option('STOP_SESSION');page.get_by_role('button',name='Send command',exact=True).click();page.wait_for_timeout(2300)
            after=sql("SELECT currency,count(*) AS count,sum(gross_amount) AS gross FROM cdrs WHERE user_id <> 'usr_sandbox' GROUP BY currency ORDER BY currency;")
            capture=shot('TC16_sandbox_stop','TC16')
            body=page.locator('body').inner_text()
            save('evidence/integration/tc16-sandbox-browser-trace.json',dict(before=before,after=after,start_text=accepted,stop_text=body))
            assert 'ACCEPTED' in accepted or 'Accepted' in accepted
            # Report the literal sandbox identity from the source separately.
            return dict(start_capture=start,stop_capture=capture,totals_before=before,totals_after=after,non_sandbox_unchanged=before==after)
        step('TC16','sandbox acknowledgement and later observation',sandbox)
        def expiry_logout():
            go('overview')
            ctx.add_cookies([{'name':'cn_portal','value':'expired.invalid.signature','domain':'localhost','path':'/'}])
            go('ledger');page.wait_for_timeout(600)
            assert page.get_by_role('heading',name='Sign in',exact=True).is_visible()
            login();go('sandbox')
            assert 'Send a command to see the request and response.' in page.locator('body').inner_text()
            page.get_by_role('button',name='Sign out',exact=True).click();page.wait_for_timeout(700)
            assert page.get_by_role('heading',name='Sign in',exact=True).is_visible()
            go('network');assert page.get_by_role('heading',name='Sign in',exact=True).is_visible()
            return dict(expired_or_invalid_cookie_denied=True,logout_protected_navigation_denied=True,trace_cleared_on_auth_loss=True,capture=shot('TC39_signed_out','TC39'))
        step('TC39','invalid session and logout boundaries',expiry_logout)
        browser.close()
    save(RESULT,out)
    print(json.dumps([(x['case_id'],x['name'],x['status']) for x in out]))

if __name__=='__main__':run()
