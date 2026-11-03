from capture import *
from ui import *
query="SELECT currency,count(*) AS count,sum(gross_amount) AS gross FROM cdrs WHERE user_id <> 'usr_sandbox' GROUP BY currency ORDER BY currency;"
sql(query)
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);page=b.new_page(viewport={'width':1440,'height':1000});login(page);page.goto('http://localhost:15173/#/sandbox');page.wait_for_timeout(800)
 options=page.locator('select').nth(0).locator('option').evaluate_all('(els)=>els.map(e=>({value:e.value,text:e.textContent}))')
 option=next(x for x in options if 'Butterworth' in x['text'] and 'DC' in x['value'] and 'AVAILABLE' in x['text'])
 page.locator('select').nth(0).select_option(option['value']);page.locator('select').nth(1).select_option('START_SESSION');shot(page,'start-command-input');page.get_by_role('button',name='Send command',exact=True).click();page.wait_for_timeout(2500);shot(page,'start-accepted-and-observed')
 page.locator('select').nth(1).select_option('STOP_SESSION');page.get_by_role('button',name='Send command',exact=True).click();page.wait_for_timeout(2500);shot(page,'stop-accepted-and-observed');sql(query)
 page.get_by_role('button',name='Sign out',exact=True).click();page.wait_for_timeout(500);login(page);page.goto('http://localhost:15173/#/sandbox');page.wait_for_timeout(700);shot(page,'history-cleared-after-signout');sql(query);b.close()
