from capture import *
ROOT=HERE.parents[1]
def restart(port=18080):
 binary=ROOT/'.runtime/server.exe'
 env=dict(os.environ,DATABASE_URL='postgres://chargenet:Chapter5LocalOnly@localhost:55432/chargenet_evidence_test?sslmode=disable',JWT_SECRET='chapter-five-disposable-local-secret',GATEWAY='ocpi',PORT=str(port),PUBLIC_BASE_URL='http://localhost:18080',PORTAL_ORIGIN='http://localhost:15173',SIM_TIME_SCALE='10',PLATFORM_FEE_PCT='5',MIN_START_BALANCE='10',FX_RATE_SOURCE='')
 script="Get-Process server -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq '"+str(binary)+"' } | ForEach-Object { Write-Output ('Kill task backend PID '+$_.Id); Stop-Process -Id $_.Id -Force }"
 args=['powershell','-NoProfile','-Command',script];p=subprocess.run(args,capture_output=True);note('$ '+subprocess.list2cmdline(args)+'\n'+p.stdout.decode()+p.stderr.decode())
 with (HERE/'backend-restart.log').open('ab',buffering=0) as log:
  process=subprocess.Popen([str(binary)],cwd=ROOT/'.work/chargenet-backend',env=env,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
 note('Started same backend executable with same database and OCPI gateway; PID '+str(process.pid))
 for _ in range(30):
  time.sleep(1)
  args=['curl.exe','--silent','--show-error','--max-time','3','http://localhost:'+str(port)+'/healthz'];p=subprocess.run(args,capture_output=True);note('$ '+subprocess.list2cmdline(args)+'\n'+p.stdout.decode()+p.stderr.decode());health=json.loads(p.stdout) if p.stdout else {}
  if isinstance(health,dict) and health.get('db')=='up':return
 raise RuntimeError('Backend did not become healthy')
