from pathlib import Path
import subprocess,datetime,os
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ENV=dict(os.environ,GOCACHE=str(ROOT/'.cache/go-build'),GOPATH=str(ROOT/'.cache/go'),TEST_DATABASE_URL='postgres://chargenet:Chapter5LocalOnly@localhost:55432/chargenet_test?sslmode=disable')
import shutil
shutil.copyfile(HERE/'migration_evidence_test.go',ROOT/'.work/chargenet-backend/internal/store/chapter_five_migration_test.go')
commands=[['go','test','-v','-count=1','-p','1','./internal/store','-run','TestChapterFiveMigrationBeforeAndAfter|TestStationGeographyAndSeedIdempotency']]
with (HERE/'migration-before-and-after.txt').open('w',encoding='utf-8',newline='') as log:
 for command in commands:
  log.write('\n'+datetime.datetime.now().astimezone().isoformat()+'\n$ '+subprocess.list2cmdline(command)+'\n');log.flush()
  p=subprocess.run(command,cwd=ROOT/'.work/chargenet-backend',env=ENV,stdout=log,stderr=subprocess.STDOUT)
  log.write('\nexit: '+str(p.returncode)+'\n');log.flush()
  print(command,'exit',p.returncode,flush=True)
