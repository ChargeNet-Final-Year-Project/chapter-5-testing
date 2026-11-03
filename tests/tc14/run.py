from partner import *
from ui import capture_page,sync_playwright,login,shot
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
    approve(admin,identity)
    operator.call('PUT','/admin/api/cpo',dict(name='Updated Chapter Five Company',baseUrl=SOURCE,contactEmail=email,colorHex='#123456',bank=dict(bankName='Chapter Five Bank',accountHolder='Test Operator',accountNo='1234567890'),payoutCycle='MONTHLY'))
    operator.call('GET','/admin/api/cpo');operator.call('GET','/admin/api/network');driver.call('GET','/api/v1/stations?cpoId='+identity)
    with sync_playwright() as browser_tools:
        browser=browser_tools.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1440,'height':1000});login(page,email,'LocalOnly123!');page.goto('http://localhost:15173/#/company');page.wait_for_timeout(800)
        page.locator('[name=name]').fill('Company Saved From Browser '+uuid.uuid4().hex[:6]);page.locator('[name=colorHex]').fill('#124578');shot(page,'company-form-input');page.get_by_role('button',name='Save changes',exact=True).click();page.wait_for_timeout(700);page.reload();page.wait_for_timeout(800);shot(page,'edited-company-reloaded');browser.close()
    operator.call('GET','/admin/api/cpo')
    capture_page(email,'network','operator-network')
finally:
    server.shutdown()
