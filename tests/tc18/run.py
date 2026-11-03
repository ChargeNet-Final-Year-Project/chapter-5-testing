from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client();c.login()
for cpo in ['cpo_voltgo','cpo_chargesync','cpo_ecowatt']:
 for country in ['MY','SG','TH']:c.call('GET','/api/v1/stations?cpoId='+cpo+'&country='+country)
sql("SELECT s.id,s.name,s.country_code,s.cpo_id,k.evse_uid,k.standard,k.power_type,k.max_power_kw,k.status FROM stations s JOIN connectors k ON k.station_id=s.id ORDER BY s.id;")
