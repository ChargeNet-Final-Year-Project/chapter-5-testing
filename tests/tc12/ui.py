"""Capture the installed browser running the actual portal."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'.tools'))
from playwright.sync_api import sync_playwright

def login(page,email='ops@voltgo.my',password='Cpo1234!'):
    page.goto('http://localhost:15173/#/login')
    page.locator('[name=email]').fill(email)
    page.locator('[name=password]').fill(password)
    page.get_by_role('button',name='Sign in',exact=True).click()
    page.wait_for_timeout(7000)

def shot(page,name):
    page.screenshot(path=str(HERE/(name+'.png')))
    (HERE/(name+'-screen.txt')).write_text(page.locator('body').inner_text(),encoding='utf-8')

def capture_page(email,route,name,password='LocalOnly123!'):
    with sync_playwright() as p:
        b=p.chromium.launch(channel='msedge',headless=True)
        page=b.new_page(viewport={'width':1440,'height':1000},timezone_id='Asia/Kuala_Lumpur')
        login(page,email,password)
        page.goto('http://localhost:15173/#/'+route)
        page.wait_for_timeout(1000)
        shot(page,name)
        b.close()
