from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client();c.login()
for query in ['country=MY','country=SG','country=TH','country=MY&cpoId=cpo_voltgo&connectorType=CCS2&minPower=40&maxPower=150','country=MY&region=Penang','country=SG&region=Penang','']:
 c.call('GET','/api/v1/stations?'+query)

for query in ['country=MY&region=Penang&cpoId=cpo_voltgo&connectorType=CCS2&minPower=40&maxPower=150','minPower=200&maxPower=50','region=Penang','country=SG&query=Marina']:
 c.call('GET','/api/v1/stations?'+query)
