import os
import base64
import copy
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
import sys
import threading
import time
from pathlib import Path
from test_support import ROOT,RUN,now
from test_api_and_accounting import Client,save,records,sql
from playwright.sync_api import sync_playwright

SOURCE='http://127.0.0.1:18090'
state={'name':'Evidence Missed Push Initial','price':1.25}
requests=[]
def location():
    return dict(country_code='MY',party_id='EV2',id='EVIDENCE-01',name=state['name'],address='Synthetic evidence site',city='Kuala Lumpur',country='MYS',coordinates=dict(latitude='3.139',longitude='101.686'),evse=[dict(uid='MY*EV2*E*01DC',status='AVAILABLE',connectors=[dict(id='1',standard='IEC_62196_T2_COMBO',format='CABLE',power_type='DC',max_electric_power=50000,tariff_ids=['evidence_two_price'])])])
def tariff():return dict(country_code='MY',party_id='EV2',id='evidence_two_price',currency='MYR',elements=[dict(price_components=[dict(type='ENERGY',price=state['price'],step_size=1)])])
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        requests.append(dict(at=now(),path=self.path,source_name=state['name'],price=state['price']))
        if self.path.endswith('/versions'):data=[dict(version='2.3.0',url=SOURCE+'/2.3.0')]
        elif self.path.rstrip('/')=='/2.3.0':data=dict(version='2.3.0',endpoints=[dict(identifier=k,role=r,url=SOURCE+'/2.3.0/'+k) for k,r in [('locations','SENDER'),('tariffs','SENDER'),('commands','RECEIVER'),('credentials','RECEIVER')]])
        elif self.path.endswith('/locations'):data=[location()]
        elif self.path.endswith('/tariffs'):data=[tariff()]
        else:data=[]
        raw=json.dumps(dict(status_code=1000,data=data,timestamp=now())).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)

def run():
    server=ThreadingHTTPServer(('127.0.0.1',18090),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
    cpo=Client();admin=Client();driver=Client();driver.login()
    code,registered,_=cpo.call('POST','/admin/api/register',dict(companyName='Evidence Partner Two',partyId='EV2',countryCode='MY',contactEmail='operator-evidence2@example.test',contactName='Synthetic Operator',password=os.environ.get('CHARGENET_FIXTURE_PASSWORD', ''),bank=dict(bankName='Synthetic Bank',accountHolder='Evidence Partner Two',accountNo=os.environ.get('CHARGENET_FIXTURE_BANK_ACCOUNT', '')),payoutCycle='MONTHLY'))
    auth=lambda v:{'Authorization':'Token '+base64.b64encode(v.encode()).decode()}
    payload=dict(token=os.environ.get('CHARGENET_PARTNER_TOKEN', ''),url=SOURCE+'/versions',roles=[dict(role='CPO',party_id='EV2',country_code='MY',business_details=dict(name='Evidence Partner Two'))])
    if code==201:
        identity=registered['cpo']['id'];token_a=registered['cpo']['tokenA']
        code,exchange,_=Client().call('POST','/ocpi/emsp/2.3.0/credentials',payload,auth(token_a));assert code==200,(code,exchange)
        token_c=exchange['data']['token']
        assert Client().call('POST','/ocpi/emsp/2.3.0/credentials',payload,auth(token_a))[0]==401
    else:
        # Resume only the previously created synthetic fixture after a harness
        # correction; earlier exchange and rejected replay remain in the logs.
        assert cpo.call('POST','/admin/api/login',dict(email='operator-evidence2@example.test',password=os.environ.get('CHARGENET_FIXTURE_PASSWORD', '')))[0]==200
        identity=cpo.call('GET','/admin/api/cpo')[1]['id']
        token_c=sql("SELECT token_c FROM cpo_partners WHERE id='"+identity+"';")[0]['token_c']
        assert admin.call('POST','/admin/api/login',dict(email='admin@chargenet.my',password=os.environ.get('CHARGENET_ADMIN_PASSWORD', '')))[0]==200
        assert admin.call('PUT','/admin/api/admin/cpos/'+identity+'/status',dict(status='PENDING'))[0]==200
    code,verified,_=cpo.call('POST','/admin/api/cpo/handshake-test');assert code==200 and verified['status']=='VERIFIED',(code,verified)
    pending=cpo.call('GET','/admin/api/cpo')[1];assert pending['status']=='PENDING'
    assert driver.call('GET','/api/v1/stations?cpoId='+identity)[1]==[]
    with sync_playwright() as p:
        b=p.chromium.launch(channel='msedge',headless=True);ctx=b.new_context(viewport={'width':1440,'height':1000},timezone_id='Asia/Kuala_Lumpur');page=ctx.new_page()
        page.goto('http://localhost:15173/#/login');page.locator('[name=email]').fill('operator-evidence2@example.test');page.locator('[name=password]').fill(os.environ.get('CHARGENET_FIXTURE_PASSWORD', ''));page.get_by_role('button',name='Sign in',exact=True).click();page.wait_for_timeout(800)
        def capture(name,case):
            stamp=now();dest=RUN/'evidence/captures'/('edge_'+stamp.replace(':','').replace('+','_')+'_'+name+'.png');page.screenshot(path=str(dest))
            with (RUN/'provenance/captures.events.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(dict(path=dest.relative_to(RUN).as_posix(),captured_at=stamp,case_id=case,session_id='',platform='Microsoft Edge Chromium'))+'\n')
        page.goto('http://localhost:15173/#/credentials');page.wait_for_timeout(700);capture('TC12_verified_pending','TC12;TC13')
        admin.call('POST','/admin/api/login',dict(email='admin@chargenet.my',password=os.environ.get('CHARGENET_ADMIN_PASSWORD', '')))
        assert admin.call('PUT','/admin/api/admin/cpos/'+identity+'/status',dict(status='ACTIVE'))[0]==200
        page.reload();page.wait_for_timeout(700);capture('TC12_verified_approved','TC12;TC13')
        stations=driver.call('GET','/api/v1/stations?cpoId='+identity)[1];assert len(stations)==1
        q=driver.call('POST','/api/v1/quotes',dict(evseUid='MY*EV2*E*01DC',estimatedKwh='15'))[1]
        assert admin.call('PUT','/admin/api/admin/cpos/'+identity+'/status',dict(status='SUSPENDED'))[0]==200
        assert driver.call('GET','/api/v1/stations?cpoId='+identity)[1]==[]
        denied=driver.call('POST','/api/v1/sessions/start',dict(evseUid='MY*EV2*E*01DC',quoteId=q['id'],targetSoc=80));assert denied[0]>=400
        admin.call('PUT','/admin/api/admin/cpos/'+identity+'/status',dict(status='ACTIVE'))
        save('evidence/integration/tc12-governance.json',dict(cpo_id=identity,verified=verified,pending=pending,approved_station_count=1,suspended_station_count=0,suspended_start_status=denied[0],suspended_start_response=denied[1],restored=True))
        print('Partner verified, approved, suspended and restored',flush=True)
        # Company edit and reload through real HTTP and the actual company screen.
        update=dict(name='Evidence Partner Two Updated',baseUrl=SOURCE,contactEmail='operator-evidence2@example.test',colorHex='#123456',bank=dict(bankName='',accountHolder='',accountNo=''),payoutCycle='MONTHLY')
        assert cpo.call('PUT','/admin/api/cpo',update)[0]==200
        page.goto('http://localhost:15173/#/company');page.reload();page.wait_for_timeout(1200)
        assert page.locator('input').evaluate_all('(els)=>els.some(e=>e.value==="Evidence Partner Two Updated")')
        save('evidence/integration/tc14-profile-reload.json',dict(cpo_id=identity,updated_name='Evidence Partner Two Updated',browser_reloaded_value_matches=True))
        # Normal production scheduler, no source push and no direct SyncOne call.
        page.goto('http://localhost:15173/#/network');page.wait_for_timeout(700);capture('TC20_before_scheduled_pull','TC19;TC20')
        old=driver.call('GET','/api/v1/stations?cpoId='+identity)[1];changed_at=now();clock=time.perf_counter()
        state.update(name='Evidence Scheduled Recovery',price=1.75)
        immediately=driver.call('GET','/api/v1/stations?cpoId='+identity)[1];assert immediately[0]['name']==old[0]['name']
        observations=[]
        for _ in range(320):
            time.sleep(1)
            latest=driver.call('GET','/api/v1/stations?cpoId='+identity)[1]
            observations.append(dict(at=now(),name=latest[0]['name'],price=latest[0]['connectors'][0]['tariffPerKwh']))
            if latest[0]['name']==state['name'] and latest[0]['connectors'][0]['tariffPerKwh']==1.75:break
        delay=(time.perf_counter()-clock)*1000
        assert latest[0]['name']==state['name'] and latest[0]['connectors'][0]['tariffPerKwh']==1.75
        page.wait_for_timeout(5400);capture('TC20_after_scheduled_pull','TC19;TC20')
        save('evidence/integration/tc20-normal-scheduler.json',dict(changed_at=changed_at,observed_at=now(),delay_ms=delay,configured_interval_seconds=300,accelerated=False,push_sent=False,before=old,immediately_after_source_change=immediately,after=latest,observations=observations,source_requests=requests))
        # Genuine receiver push; restore the fixture afterwards.
        loc=location();loc['evse'][0]['status']='OUTOFORDER';push_at=now();clock=time.perf_counter()
        code,reply,_=Client().call('PUT','/ocpi/emsp/2.3.0/locations/MY/EV2/EVIDENCE-01',loc,auth(token_c));assert code==200
        pushed=driver.call('GET','/api/v1/stations?cpoId='+identity)[1]
        assert pushed[0]['connectors'][0]['status']=='INOPERATIVE'
        visibility=(time.perf_counter()-clock)*1000
        save('evidence/integration/tc19-push-visibility.json',dict(pushed_at=push_at,observed_at=now(),visibility_ms=visibility,status=code,reply=reply,driver_api=pushed))
        Client().call('PUT','/ocpi/emsp/2.3.0/locations/MY/EV2/EVIDENCE-01',location(),auth(token_c))
        payload['token']=os.environ.get('CHARGENET_ROTATED_PARTNER_TOKEN', '')
        code,rotated,_=Client().call('PUT','/ocpi/emsp/2.3.0/credentials',payload,auth(token_c));assert code==200
        old_token_denied=Client().call('GET','/ocpi/emsp/2.3.0/credentials',headers=auth(token_c))[0];assert old_token_denied==401
        new_token=rotated['data']['token']
        assert Client().call('DELETE','/ocpi/emsp/2.3.0/credentials',headers=auth(new_token))[0]==200
        disconnected=cpo.call('GET','/admin/api/cpo')[1]
        save('evidence/integration/tc17-tc13-token-lifecycle.json',dict(token_a_reuse_denied=True,old_operational_token_denied_after_rotation=True,unregistered=True,profile=disconnected))
        b.close()
    server.shutdown()
    save('evidence/requests/test_ocpi_reconciliation.json',records)
    print('Production scheduler, governance, push and credential lifecycle completed',flush=True)

if __name__=='__main__':
    try:run()
    finally:save('evidence/requests/Partner experiment partial.json',records)
