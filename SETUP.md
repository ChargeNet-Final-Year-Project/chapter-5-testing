# Chapter 5 test setup

The tests use application source exports in `.work`: backend `b72dedde0c287bd144fd05c7b61564a9d18696ca`, mobile `ccfc7aa7c4242f516ca0b588e9d4cf01dde3ee83`, portal `e604613f4697bf1e2fd732ddde859e1393fa7f6b`. TC01 includes additional Go checks; TC44 records migration snapshots.

Use Windows, Python 3.12, Go 1.26.5, Flutter 3.47.1/Dart 3.13.1, Node 22.13.1/npm 10.9.2, Docker with PostgreSQL 16, and Android SDK/ADB. Browser capture uses installed Edge and Firefox; this run used Firefox 158.0.1. Python browser packages are in `.tools`; reinstall with `python -m pip install --target .tools playwright selenium pillow` if needed.

Create `.work/chargenet-backend`, `.work/chargenet-mobile` and `.work/chargenet-portal` from the corresponding application repositories at the revisions above. These source exports, downloaded tools, build caches and runtime files are local prerequisites and are excluded from Git. Install the portal dependencies with `npm ci` in `.work/chargenet-portal` and the mobile dependencies with `flutter pub get` in `.work/chargenet-mobile`.

From this folder, prepare the disposable services once:

```powershell
docker run -d --name chargenet-ch5-new-postgres -e POSTGRES_USER=chargenet -e POSTGRES_PASSWORD=Chapter5LocalOnly -e POSTGRES_DB=chargenet_test -p 127.0.0.1:55432:5432 postgres:16-alpine
docker exec chargenet-ch5-new-postgres psql -U chargenet -d postgres -c 'CREATE DATABASE chargenet_evidence_test;'
cd tests/tc03; python run.py; cd ../..
./start-services.ps1
```

For an existing container, use `docker start chargenet-ch5-new-postgres`; do not recreate its database. Backend regression uses `chargenet_test`; runtime cases use the separate `chargenet_evidence_test`. Never point these helpers at application history. Runtime ports are 18080/15173, OCPI source experiments use 18090, simulation scale is 10, fee is 5%, normal synchronization is 300 seconds. Run runtime cases sequentially. Stop the task's backend/portal processes and `docker stop chargenet-ch5-new-postgres` when finished.

Run `python run.py` from an individual case folder; use the additional command named in its README for mobile/browser captures. All local inputs and imports stay in that case. Browser packages and application exports are common tool/application prerequisites. Helpers keep actual curl commands, request bodies, HTTP status and response bodies in `requests.txt`; regression helpers write direct command output. They do not infer test verdicts. Local disposable credentials remain visible.

For Android, start `Medium_Phone`, install `.work/chargenet-mobile/build/app/outputs/flutter-apk/app-debug.apk`, complete onboarding, and sign in as `demo@chargenet.my` / `Demo1234!`. The APK targets `http://10.0.2.2:18080`. ADB defaults to `C:/Users/ongji/AppData/Local/Android/Sdk/platform-tools/adb.exe`; set `ADB_BIN` if different. Coordinate helpers require 1080 x 2400 and density 420; screenshots must be inspected after each action. Location permission and Penang simulator coordinates are test setup.

Each folder under `tests/tc01` through `tests/tc44` has a README with its commands, observations and evidence links.
