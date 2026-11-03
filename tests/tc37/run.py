from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
a=Client('anonymous')
for path in ['/admin/api/cpo','/admin/api/network','/admin/api/cdrs','/admin/api/admin/cpos']:a.call('GET',path)
b=Client('operator');b.call('POST','/admin/api/login',dict(email='ops@voltgo.my',password='Cpo1234!'))
for path in ['/admin/api/network','/admin/api/admin/cpos','/admin/api/cdrs?cpoId=cpo_chargesync']:b.call('GET',path)
b.call('PUT','/admin/api/admin/cpos/cpo_chargesync/status',dict(status='ACTIVE'))

driver=Client('fixture');driver.register();driver.fund(500)
for operator in ['cpo_voltgo','cpo_chargesync']:
 station,k=driver.pick(cpo=operator);q=driver.quote(k);session=driver.start(k,q);driver.positive(session);receipt=driver.call('POST','/api/v1/sessions/'+session['id']+'/stop');accounting(session['id']);b.call('GET','/admin/api/cdrs/'+receipt['cdrId']);accounting(session['id'])
