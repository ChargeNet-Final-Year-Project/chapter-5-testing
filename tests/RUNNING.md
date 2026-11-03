# Reproducing the tests

The checked-in results record the original executions. Reproduction creates new observations; do not replace a recorded result with an expectation or a successful build alone.

## Requirements

The recorded environment used Windows, Python 3.12, Go 1.26.5, PostgreSQL 16, Flutter 3.47.1 / Dart 3.13.1 and Node 22.13.1. Android device interactions used an Android 17 emulator, 1080 x 2400 at density 420, with separate 320dp/200% text checks. Browser evidence used Microsoft Edge and Firefox.

Use an isolated workspace. The application repositories must be checked out separately; their recorded SHAs are `ca5052217633bb405ceb52f5e98e9b61ccd060ba` (backend), `ccfc7aa7c4242f516ca0b588e9d4cf01dde3ee83` (mobile) and `e3e7dbc4d72b3e6fda8c8c0b9897e5d83f0152f1` (portal). The additional backend checks were executed at `ca5052217633bb405ceb52f5e98e9b61ccd060ba`, including the retained additional test files.

From the root of this repository:

```text
python -m venv .venv
```

Activate the environment, then install the optional browser dependencies:

```text
python -m pip install -r requirements.txt
```

The recorded browser procedures launch installed Microsoft Edge with `channel='msedge'`. Firefox checks use Selenium and an installed Firefox; set `FIREFOX_BIN` if it cannot be discovered. Android procedures require `adb`, an installed debug APK and the expected starting screen. Set `ADB_BIN`, `FLUTTER_BIN` or `ANDROID_SERIAL` when needed.

## Configuration and isolated databases

Copy `.env.example` to `.env` and fill in disposable values. `.env` is ignored by Git. `CHARGENET_WORKSPACE` is the parent directory containing `chargenet-backend`, `chargenet-mobile` and `chargenet-portal`. Credentials must match the synthetic accounts in the disposable runtime fixtures.

Set:

- `CHARGENET_TEST_DB_PASSWORD`: password for the dedicated PostgreSQL service.
- `TEST_DATABASE_URL`: PostgreSQL URL ending in `/chargenet_test`, using the configured local database port.
- `DATABASE_URL`: a separate URL ending in `/chargenet_evidence_test`.
- `CHARGENET_JWT_SECRET` and the `CHARGENET_*_PASSWORD` variables: disposable runtime signing/account values.

Start the dedicated database service:

```text
docker compose up -d --wait postgres
```

The default host port is **55433**, bound to localhost. Initialization creates `chargenet_test` and `chargenet_evidence_test`. Automated SQL tests clear their fixtures; runtime journeys use the separate evidence database. The runner rejects application and evidence databases as destructive-test targets. Do not use demonstration history or production data.

## Backend regression and the additional Go tests

The backend's original tracked tests provide the shared harness and application packages. Prepare a separate checkout from an existing local backend clone:

```text
python tests/prepare_backend_checkout.py --source ../chargenet-backend
```

This checks out the recorded commit into `.work/backend` and installs the additional tests. It refuses to overwrite an existing destination or a different test file. It leaves the source checkout unchanged.

Run:

```text
python tests/run_checks.py backend --checkout .work/backend
```

This executes `go test -json -count=1 -p 1 ./...`, `go vet ./...` and `go build ./...`. Serial package execution is required because SQL tests share and clear disposable fixtures. Test-level skips prevent a successful verification result; packages without test files are counted separately.

The additional files cover simultaneous competing starts, start-failure accounting, zero-energy repeated stops, uncertain remote stops followed by confirmed settlement, and accelerated scheduler recovery. The accelerated test is separate from the recorded normal 300-second scheduler experiment.

## Mobile and portal regression

Use fresh application checkouts at the recorded revisions, then run:

```text
python tests/run_checks.py mobile --checkout ../chargenet-mobile
python tests/run_checks.py portal --checkout ../chargenet-portal
```

The mobile runner resolves locked dependencies, performs analysis, runs machine-readable tests with concurrency one and builds a debug APK. The portal runner performs the locked dependency installation, TypeScript check and production build. These commands preserve output, errors, timestamps and exit codes in the new run directory.

## Runtime, API, browser and device procedures

Install the portal dependencies and configure the application checkout paths first. Set a shared `CHARGENET_RUN_DIR` for related runtime commands; otherwise each process creates its own timestamped run directory.

```text
python tests/run_test_services.py
```

The disposable backend listens on port **18080**, the portal on **15173**, with `GATEWAY=ocpi`, time scale 10, fee 5% and a normal 300-second synchronization interval. The service runner builds the backend from the configured checkout. Use the recorded checkout for exact reproduction; current application revisions may behave differently.

Build the mobile debug app with `API_BASE_URL=http://10.0.2.2:18080` and install it on the emulator. Android interactions require the recorded screen dimensions, the intended selected station and a signed-in synthetic driver. Read the relevant case procedure in [CASES.md](CASES.md) before running a device journey.

| Procedure | Command |
|---|---|
| API, ownership, replay and accounting checks | `python tests/test_api_and_accounting.py run_checks` |
| Active-session and settlement process restart | `python tests/test_api_and_accounting.py restart_checks` |
| Partner exchange and normal missed-push recovery | `python tests/test_ocpi_reconciliation.py` |
| Portal browser workflows | `python tests/test_portal_browser.py` |
| Reporting fixtures and currency-separated exports | `python tests/test_portal_reporting.py` |
| Expired sessions, token display and administrator layouts | `python tests/test_portal_security.py` |
| Firefox layout sample | `python tests/test_firefox_layout.py` |
| Device size, density and text settings | `python tests/android_controls.py device` |
| Driver journey on an already selected operator station | `python tests/test_mobile_journeys.py voltgo` (repeat for `chargesync`, `ecowatt` with the same account) |
| Complete connectivity loss and explicit live-update retry | `python tests/test_mobile_reconnection.py` |
| Start-to-first-positive telemetry | `python tests/measure_response_times.py` |
| Joined accounting export without starting another charge | `python tests/export_session_accounting.py` |

Reporting/security browser checks expect the 26 October 2026 reporting fixtures produced by the reporting utility. The controlled OCPI source uses port **18090** and may wait for the normal scheduler interval. These tools write synthetic records, rotate disposable credentials or interrupt test services; use only the isolated runtime.

Stop the service runner with Ctrl+C or create `build/stop-services` inside the shared run directory. A restart experiment uses its `build/restart_backend` marker to kill and reconstruct only that runner's backend process.

