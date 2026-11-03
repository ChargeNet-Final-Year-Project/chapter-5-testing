from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client();c.register();c.call('GET','/api/v1/wallet');c.call('GET','/api/v1/wallet/transactions')
key=uuid.uuid4().hex
for i in range(2):c.call('POST','/api/v1/wallet/topup',dict(amount=100,paymentMethod='Credit Card'),{'Idempotency-Key':key})
for body in [dict(amount=-1,paymentMethod='Credit Card'),dict(amount=10,paymentMethod='invalid')]:c.call('POST','/api/v1/wallet/topup',body)
c.call('GET','/api/v1/wallet');c.call('GET','/api/v1/wallet/transactions')
