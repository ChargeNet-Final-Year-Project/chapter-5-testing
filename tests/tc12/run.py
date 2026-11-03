from partner import *
from ui import capture_page,sync_playwright,login,shot
server,operator,admin,driver,identity,token_a,token_c,payload,email=setup()
try:
    with sync_playwright() as browser_tools:
        browser=browser_tools.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1440,'height':1000});login(page,email,'LocalOnly123!');page.goto('http://localhost:15173/#/credentials');page.wait_for_timeout(700);page.get_by_role('button',name='Run handshake test',exact=True).click();page.wait_for_timeout(1000);shot(page,'verified-pending');browser.close()
    operator.call('GET','/admin/api/cpo');driver.call('GET','/api/v1/stations?cpoId='+identity)
    with sync_playwright() as browser_tools:
        browser=browser_tools.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1440,'height':1000});login(page,'admin@chargenet.my','Admin1234!');page.goto('http://localhost:15173/#/admin');page.wait_for_timeout(700)
        row=page.locator('tr').filter(has_text=PARTY);row.scroll_into_view_if_needed();shot(page,'admin-approval-input');row.get_by_role('button',name='Approve',exact=True).click();page.wait_for_timeout(300)
        if page.get_by_role('dialog').count():page.get_by_role('dialog').get_by_role('button',name='Approve',exact=True).click()
        page.wait_for_timeout(800);row.scroll_into_view_if_needed();shot(page,'admin-approval-result');browser.close()
    operator.call('GET','/admin/api/cpo');stations=driver.call('GET','/api/v1/stations?cpoId='+identity)
    capture_page(email,'credentials','verified-approved')
    k=stations[0]['connectors'][0];q=driver.quote(k)
    admin.call('PUT','/admin/api/admin/cpos/'+identity+'/status',dict(status='SUSPENDED'));driver.call('GET','/api/v1/stations?cpoId='+identity);driver.start(k,q);approve(admin,identity)
finally:
    server.shutdown()
