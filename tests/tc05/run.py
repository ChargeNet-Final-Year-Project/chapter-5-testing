from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client(); c.login()
for country,cpo in [('MY','cpo_voltgo'),('SG','cpo_chargesync'),('TH','cpo_ecowatt')]:
 c.pick(country,cpo)
sql("SELECT s.id,s.name,s.country_code,s.cpo_id,k.evse_uid,k.standard,k.power_type,k.max_power_kw,k.status FROM stations s JOIN connectors k ON k.station_id=s.id ORDER BY s.id;")
