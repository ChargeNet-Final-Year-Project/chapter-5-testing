"""ADB actions and unaltered emulator screenshots. Coordinates use 1080 x 2400."""
from capture import *
ADB=os.environ.get('ADB_BIN',r'C:\Users\ongji\AppData\Local\Android\Sdk\platform-tools\adb.exe')

def adb(*args):
    command=[ADB,*map(str,args)]
    result=subprocess.run(command,capture_output=True,timeout=40)
    note('$ '+subprocess.list2cmdline(command)+'\n'+result.stdout.decode('utf-8','replace')+result.stderr.decode('utf-8','replace')+'\nexit: '+str(result.returncode))
    return result.stdout

def tap(x,y):
    adb('shell','input','tap',x,y)
    time.sleep(.6)

def fill(x,y,value):
    tap(x,y)
    adb('shell','input','keyevent','123')
    adb('shell','input','keyevent',*(['67']*80))
    adb('shell','input','text',value.replace(' ','%s'))
    adb('shell','input','keyevent','4')
    time.sleep(.5)

def shot(name):
    command=[ADB,'exec-out','screencap','-p']
    result=subprocess.run(command,capture_output=True,timeout=30)
    if result.returncode:raise RuntimeError(result.stderr.decode())
    (HERE/(name+'.png')).write_bytes(result.stdout)
    note('$ '+subprocess.list2cmdline(command)+' > '+name+'.png (unaltered PNG; '+str(len(result.stdout))+' bytes)')

def launch():
    adb('shell','am','start','-n','com.chargenet.mobile/com.example.chargenet_mobile.MainActivity')
    time.sleep(2)

if __name__=='__main__':
    launch();shot('current-screen')
