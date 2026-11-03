from ui import *
from capture import note
import os,time,subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
os.environ['SE_CACHE_PATH']=str(HERE.parents[1]/'.cache/selenium');os.environ['MOZ_HEADLESS']='1'
opt=Options();opt.add_argument('-headless');opt.binary_location=r'C:/Program Files/Mozilla Firefox/firefox.exe'
service=Service(log_output=str(HERE/'firefox-driver.txt'));service.creation_flags=subprocess.CREATE_NO_WINDOW
driver=webdriver.Firefox(options=opt,service=service)
try:
 note('Firefox version: '+driver.capabilities['browserVersion']);driver.get('http://localhost:15173/#/login');time.sleep(1);driver.find_element(By.NAME,'email').send_keys('ops@voltgo.my');driver.find_element(By.NAME,'password').send_keys('Cpo1234!');driver.find_element(By.CSS_SELECTOR,'button[type=submit]').click();time.sleep(7)
 for width in [1440,390]:
  driver.set_window_size(width,1000)
  for route in ['overview','ledger','network','credentials']:
   driver.get('http://localhost:15173/#/'+route);time.sleep(1);driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB);note(str(driver.execute_script('return {viewport:innerWidth,scroll:document.documentElement.scrollWidth,focus:document.activeElement.outerHTML}')));driver.save_screenshot(str(HERE/('firefox-'+str(width)+'-'+route+'.png')));(HERE/('firefox-'+str(width)+'-'+route+'-screen.txt')).write_text(driver.find_element(By.TAG_NAME,'body').text,encoding='utf-8')
finally:driver.quit()
