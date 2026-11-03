import json,os,sys,time,subprocess
from pathlib import Path
from test_support import ROOT,RUN,now
from test_api_and_accounting import save
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

def run():
    os.environ.setdefault('SE_CACHE_PATH',str(Path.home()/'.cache/selenium'))
    os.environ['MOZ_HEADLESS']='1'
    opt=Options();opt.add_argument('-headless')
    if os.environ.get('FIREFOX_BIN'):opt.binary_location=os.environ['FIREFOX_BIN']
    service=Service(log_output=str(RUN/'evidence/portal/Firefox driver.log'));service.creation_flags=getattr(subprocess,'CREATE_NO_WINDOW',0)
    driver=webdriver.Firefox(options=opt,service=service)
    outcomes=[]
    try:
        driver.get('http://localhost:15173/#/login');time.sleep(1)
        driver.find_element(By.NAME,'email').send_keys('ops@voltgo.my');driver.find_element(By.NAME,'password').send_keys(os.environ.get('CHARGENET_OPERATOR_PASSWORD', ''));driver.find_element(By.CSS_SELECTOR,'button[type=submit]').click();time.sleep(1)
        for width in [1440,390]:
            driver.set_window_size(width,1000)
            for route in ['overview','ledger','network','credentials']:
                driver.get('http://localhost:15173/#/'+route);time.sleep(.7)
                driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB)
                metrics=driver.execute_script('return {viewport:innerWidth,scroll:document.documentElement.scrollWidth,focus:document.activeElement.tagName}')
                assert driver.find_element(By.TAG_NAME,'h1').text!='Sign in'
                stamp=now();dest=RUN/'evidence/captures'/('firefox_'+stamp.replace(':','').replace('+','_')+f'_{width}_{route}.png');driver.save_screenshot(str(dest))
                with (RUN/'provenance/captures.events.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(dict(path=dest.relative_to(RUN).as_posix(),captured_at=stamp,case_id='TC42',platform='Firefox',session_id=''))+'\n')
                outcomes.append(dict(route=route,requested_outer_width=width,metrics=metrics,browser_version=driver.capabilities['browserVersion'],capture=dest.relative_to(RUN).as_posix(),status='Pass' if metrics['scroll']<=metrics['viewport'] else 'Fail'))
        save('evidence/portal/firefox-results.json',outcomes)
        assert all(x['status']=='Pass' for x in outcomes)
        print('Firefox layout/navigation cases',len(outcomes))
    finally:driver.quit()

if __name__=='__main__':run()
