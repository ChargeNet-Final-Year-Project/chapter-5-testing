import os
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from test_support import ROOT,RUN,ADB,now
sys.stdout.reconfigure(encoding='utf8',errors='replace')

def adb(*args,binary=False):
    p=subprocess.run([ADB,'-s',os.environ.get('ANDROID_SERIAL','emulator-5554'),*map(str,args)],capture_output=True,timeout=30,check=True)
    return p.stdout if binary else p.stdout.decode('utf8','replace').strip()
def tap(x,y):adb('shell','input','tap',x,y);time.sleep(.6)
def swipe(x1,y1,x2,y2,ms=500):adb('shell','input','swipe',x1,y1,x2,y2,ms);time.sleep(.7)
def back():adb('shell','input','keyevent',4);time.sleep(.5)
def input_text(value):adb('shell','input','text',value.replace(' ','%s'));time.sleep(.3)
def nodes():
    adb('shell','uiautomator','dump','/sdcard/chapter5-window.xml')
    raw=adb('shell','cat','/sdcard/chapter5-window.xml')
    for secret in [os.environ.get('CHARGENET_DRIVER_PASSWORD', ''),os.environ.get('CHARGENET_OPERATOR_PASSWORD', ''),os.environ.get('CHARGENET_ADMIN_PASSWORD', '')]:
        if secret:raw=raw.replace(secret,'[REDACTED]')
    (RUN/'evidence/mobile/Current ui.xml').write_text(raw,encoding='utf8')
    return list(ET.fromstring(raw).iter('node'))
def dump():
    for n in nodes():
        label=n.get('text') or n.get('content-desc') or n.get('hint')
        if label:print(n.get('bounds'),repr(label))
def click(label,partial=False):
    for n in nodes():
        labels=[n.get('text',''),n.get('content-desc',''),n.get('hint','')]
        if label in labels or any(v.startswith(label+'\n') for v in labels) or (partial and any(label in v for v in labels)):
            x1,y1,x2,y2=map(int,re.findall(r'\d+',n.get('bounds')));tap((x1+x2)//2,(y1+y2)//2);return
    raise ValueError('Control not found: '+label)
def click_last(label):
    matched=[n for n in nodes() if label in [n.get('text',''),n.get('content-desc',''),n.get('hint','')]]
    if not matched:raise ValueError('Control not found: '+label)
    n=matched[-1];x1,y1,x2,y2=map(int,re.findall(r'\d+',n.get('bounds')));tap((x1+x2)//2,(y1+y2)//2)
def shot(name,case='',session=''):
    stamp=now();path=RUN/'evidence/captures'/('android_'+stamp.replace(':','').replace('+','_')+'_'+name+'.png')
    path.write_bytes(adb('exec-out','screencap','-p',binary=True))
    with (RUN/'provenance/captures.events.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(dict(path=path.relative_to(RUN).as_posix(),captured_at=stamp,case_id=case,session_id=session,platform='Android emulator'))+'\n')
    print('CAPTURE',path.relative_to(RUN))
def device():
    data={x:adb('shell',*args) for x,args in {'size':['wm','size'],'density':['wm','density'],'font_scale':['settings','get','system','font_scale'],'android':['getprop','ro.build.version.release'],'model':['getprop','ro.product.model']}.items()}
    (RUN/'provenance/android-environment.json').write_text(json.dumps(data,indent=2));print(data)
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Inspect the configured Android emulator.')
    parser.add_argument('action', choices=['device', 'dump'])
    args = parser.parse_args()
    {'device': device, 'dump': dump}[args.action]()
