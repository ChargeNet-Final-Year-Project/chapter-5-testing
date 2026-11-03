"""Controlled OCPI source; the application receives real HTTP requests via curl."""
from capture import *
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import base64

PARTY = ''.join(__import__('secrets').choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(3))
SOURCE = 'http://127.0.0.1:18090'
state = {'name': 'Controlled Chapter Five Station', 'price': 1.25, 'status': 'AVAILABLE'}

def location():
    return dict(country_code='MY', party_id=PARTY, id='LOCAL01', name=state['name'], address='Chapter Five test site', city='Kuala Lumpur', country='MYS', coordinates=dict(latitude='3.139', longitude='101.686'), evse=[dict(uid='MY*'+PARTY+'*E*01DC', status=state['status'], connectors=[dict(id='1', standard='IEC_62196_T2_COMBO', format='CABLE', power_type='DC', max_electric_power=50000, tariff_ids=['price-'+PARTY])])])

def tariff():
    return dict(country_code='MY', party_id=PARTY, id='price-'+PARTY, currency='MYR', elements=[dict(price_components=[dict(type='ENERGY', price=state['price'], step_size=1)])])

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path.endswith('/versions'):
            data = [dict(version='2.3.0', url=SOURCE+'/2.3.0')]
        elif self.path.rstrip('/') == '/2.3.0':
            data = dict(version='2.3.0', endpoints=[dict(identifier=k, role=r, url=SOURCE+'/2.3.0/'+k) for k,r in [('locations','SENDER'),('tariffs','SENDER'),('commands','RECEIVER'),('credentials','RECEIVER')]])
        elif self.path.rstrip('/').endswith('/locations'):
            data = [location()]
        elif self.path.rstrip('/').endswith('/tariffs'):
            data = [tariff()]
        else:
            data = []
        raw = json.dumps(dict(status_code=1000, data=data, timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat())).encode()
        note('SOURCE GET '+self.path+' -> '+raw.decode())
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

def auth(token):
    return {'Authorization': 'Token '+base64.b64encode(token.encode()).decode()}

def setup():
    server = ThreadingHTTPServer(('127.0.0.1',18090),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    operator = Client('operator')
    email = HERE.name+'-'+uuid.uuid4().hex[:8]+'@example.test'
    registered = operator.call('POST','/admin/api/register',dict(companyName='Controlled '+HERE.name+' '+uuid.uuid4().hex[:6],partyId=PARTY,countryCode='MY',contactEmail=email,contactName='Test Operator',password='LocalOnly123!',bank=dict(bankName='Chapter Five Bank',accountHolder='Test Operator',accountNo='1234567890'),payoutCycle='MONTHLY'))
    identity=registered['cpo']['id']
    token_a=registered['cpo']['tokenA']
    payload=dict(token='local-source-'+uuid.uuid4().hex,url=SOURCE+'/versions',roles=[dict(role='CPO',party_id=PARTY,country_code='MY',business_details=dict(name='Controlled '+HERE.name))])
    if HERE.name=='tc13':
        from ui import sync_playwright,login,shot
        with sync_playwright() as browser_tools:
            browser=browser_tools.chromium.launch(channel='msedge',headless=True)
            context=browser.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'])
            page=context.new_page();login(page,email,'LocalOnly123!');page.goto('http://localhost:15173/#/credentials');page.wait_for_timeout(1000);shot(page,'unused-token-masked')
            page.get_by_role('button',name='Reveal',exact=True).click();shot(page,'unused-token-revealed')
            page.locator('.field').filter(has_text='Token A (one-time registration token)').get_by_role('button',name='Copy',exact=True).click();note('Browser clipboard returned: '+page.evaluate('navigator.clipboard.readText()'))
            page.get_by_role('button',name='Hide',exact=True).click();shot(page,'unused-token-hidden')
            browser.close()
    exchange=Client('exchange').call('POST','/ocpi/emsp/2.3.0/credentials',payload,auth(token_a))
    token_c=exchange['data']['token']
    operator.call('POST','/admin/api/cpo/handshake-test')
    admin=Client('admin');admin.call('POST','/admin/api/login',dict(email='admin@chargenet.my',password='Admin1234!'))
    driver=Client('driver');driver.login()
    return server,operator,admin,driver,identity,token_a,token_c,payload,email

def approve(admin,identity):
    return admin.call('PUT','/admin/api/admin/cpos/'+identity+'/status',dict(status='ACTIVE'))
