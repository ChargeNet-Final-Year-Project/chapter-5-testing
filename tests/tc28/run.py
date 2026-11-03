from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
from concurrent.futures import ThreadPoolExecutor
c=Client();c.register();c.fund();station,k=c.pick();q=c.quote(k);s=c.start(k,q);c.positive(s);accounting(s['id'])
barrier=threading.Barrier(2)
def stop(_):
 other=Client(uuid.uuid4().hex);other.token=c.token;barrier.wait();return other.call('POST','/api/v1/sessions/'+s['id']+'/stop')
with ThreadPoolExecutor(2) as p:list(p.map(stop,[1,2]))
accounting(s['id']);c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id']);c.call('GET','/api/v1/wallet/transactions')
