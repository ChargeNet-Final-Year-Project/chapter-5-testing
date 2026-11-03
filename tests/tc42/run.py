from ui import *
from capture import note
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);page=b.new_page(timezone_id='Asia/Kuala_Lumpur');login(page)
 note('Edge browser version: '+b.version)
 for width in [1440,390]:
  page.set_viewport_size({'width':width,'height':1000})
  for route in ['overview','ledger','network','credentials']:
   page.goto('http://localhost:15173/#/'+route);page.wait_for_timeout(800);page.keyboard.press('Tab');note(str(page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,focus:document.activeElement.outerHTML})')));shot(page,str(width)+'-'+route)
 page.context.clear_cookies();login(page,'admin@chargenet.my','Admin1234!')
 for width in [1440,390]:
  page.set_viewport_size({'width':width,'height':1000});page.goto('http://localhost:15173/#/admin');page.wait_for_timeout(800);page.keyboard.press('Tab');shot(page,str(width)+'-admin')
 b.close()
