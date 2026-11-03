from mobile import *
from importlib.util import spec_from_file_location,module_from_spec
# Local functions only; avoid executing the full discovery/profile capture again.
source=(HERE/'android-layout.py').read_text();exec(source[:source.index("restore();adb")])
restore();adb('shell','am','force-stop','com.chargenet.mobile');launch();time.sleep(12);tap(180,2250);tap(840,160);fill(450,160,'Batu Kawan');time.sleep(2);shot('estimate-search-input');tap(450,325);time.sleep(2);shot('estimate-station-input');adb('shell','input','swipe','700','1970','700','1100','600');time.sleep(2);shot('estimate-connector-input');tap(540,1555);time.sleep(2);shot('estimate-normal-input');layouts('estimate')
