from capture import *
import statistics,math,csv
admin=Client('admin');admin.call('POST','/admin/api/login',dict(email='admin@chargenet.my',password='Admin1234!'))
note('Hide only disposable partners created by this evidence run to restore the original 38-station discovery fixture.')
for row in sql("SELECT id FROM cpo_partners WHERE id NOT IN ('cpo_voltgo','cpo_chargesync','cpo_ecowatt') AND status='ACTIVE';"):
 admin.call('PUT','/admin/api/admin/cpos/'+row['id']+'/status',dict(status='SUSPENDED'))
c=Client();c.login();samples=[]
for i in range(35):
 args=['curl.exe','--silent','--show-error','--max-time','10','-i','-H','Authorization: Bearer '+c.token,'--write-out','\nCURL_TIME_TOTAL:%{time_total}\nHTTP_STATUS:%{http_code}\n',BASE+'/api/v1/stations']
 p=subprocess.run(args,capture_output=True);raw=p.stdout.decode();note('$ '+subprocess.list2cmdline(args)+'\n'+raw+p.stderr.decode())
 timing=float(raw.split('CURL_TIME_TOTAL:')[-1].splitlines()[0])*1000;status=int(raw.split('HTTP_STATUS:')[-1].splitlines()[0]);payload=raw.split('\r\n\r\n',1)[1].split('\nCURL_TIME_TOTAL:')[0];stations=json.loads(payload)
 samples.append(dict(sample=i+1,warmup=i<5,http_status=status,elapsed_ms=timing,station_count=len(stations)))
with (HERE/'timing-samples.csv').open('w',newline='') as file:
 writer=csv.DictWriter(file,fieldnames=list(samples[0]));writer.writeheader();writer.writerows(samples)
times=[x['elapsed_ms'] for x in samples[5:] if x['http_status']==200]
note(f'5 warmups; 30 measured sequential HTTP transfers; median {statistics.median(times):.3f} ms; nearest-rank p95 {sorted(times)[math.ceil(.95*len(times))-1]:.3f} ms; errors {sum(x["http_status"]!=200 for x in samples[5:])}; station count {len(stations)}. Local descriptive measurement, no SLA.')
c.fund();st,k=c.pick();q=c.quote(k);start=time.perf_counter();s=c.start(k,q)
args=['curl.exe','--silent','--show-error','-N','--max-time','12','-H','Authorization: Bearer '+c.token,BASE+'/api/v1/sessions/'+s['id']+'/stream'];note('$ '+subprocess.list2cmdline(args));process=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
try:
 for line in process.stdout:
  elapsed=(time.perf_counter()-start)*1000;note(f'received at {elapsed:.3f} ms: '+line.rstrip())
  if line.startswith('data:'):
   try:frame=json.loads(line[5:])
   except ValueError:continue
   if isinstance(frame,dict) and frame.get('kwhDelivered',0)>0:note(f'Start-to-first-positive-SSE: {elapsed:.3f} ms');break
finally:
 process.terminate();process.wait(timeout=10)
c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])
