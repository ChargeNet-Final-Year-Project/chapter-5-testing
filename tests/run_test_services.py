import json
import os
import shutil
import subprocess
import time
from test_support import ROOT, RUN, RUNTIME_DSN, now, validate_runtime_dsn


def main():
    validate_runtime_dsn(RUNTIME_DSN)
    if not os.environ.get('CHARGENET_JWT_SECRET'):
        raise ValueError('Set CHARGENET_JWT_SECRET before starting the disposable runtime')
    flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
    binary = RUN / 'build' / ('server.exe' if os.name == 'nt' else 'server')
    subprocess.run(['go', 'build', '-o', str(binary), './cmd/server'], cwd=ROOT / 'chargenet-backend', check=True, creationflags=flags)
    backend_env = {**os.environ, 'DATABASE_URL': RUNTIME_DSN, 'GATEWAY': 'ocpi', 'PORT': '18080', 'PUBLIC_BASE_URL': 'http://localhost:18080', 'PORTAL_ORIGIN': 'http://localhost:15173', 'SIM_TIME_SCALE': '10', 'PLATFORM_FEE_PCT': '5', 'MIN_START_BALANCE': '10', 'FX_RATE_SOURCE': '', 'JWT_SECRET': os.environ['CHARGENET_JWT_SECRET']}
    backend_log = (RUN / 'evidence/integration/server.log').open('ab', buffering=0)
    portal_log = (RUN / 'evidence/portal/server.log').open('ab', buffering=0)
    lifecycle = RUN / 'provenance/service-lifecycle.events.jsonl'
    def start_backend():
        process = subprocess.Popen([str(binary)], cwd=ROOT / 'chargenet-backend', env=backend_env, stdout=backend_log, stderr=backend_log, creationflags=flags)
        with lifecycle.open('a', encoding='utf8') as file:
            file.write(json.dumps(dict(event='backend_start', pid=process.pid, at=now(), gateway='ocpi', database='chargenet_evidence_test')) + '\n')
        return process
    backend = start_backend()
    portal = None
    try:
        portal_path = ROOT / 'chargenet-portal'
        portal = subprocess.Popen([shutil.which('node') or 'node', str(portal_path / 'node_modules/vite/bin/vite.js'), '--host', '127.0.0.1', '--port', '15173', '--strictPort'], cwd=portal_path, env={**os.environ, 'VITE_API_BASE_URL': 'http://localhost:18080'}, stdout=portal_log, stderr=portal_log, creationflags=flags)
        print(json.dumps(dict(backend_pid=backend.pid, portal_pid=portal.pid, run_directory=str(RUN))), flush=True)
        while not (RUN / 'build/stop-services').exists():
            marker = RUN / 'build/restart_backend'
            if marker.exists():
                old = backend.pid
                backend.kill()
                backend.wait(timeout=15)
                with lifecycle.open('a', encoding='utf8') as file:
                    file.write(json.dumps(dict(event='backend_abrupt_kill', pid=old, at=now())) + '\n')
                backend = start_backend()
                marker.unlink()
            if backend.poll() is not None or portal.poll() is not None:
                raise RuntimeError('A runtime service exited; inspect the retained service logs')
            time.sleep(.25)
    finally:
        for process in [backend, portal]:
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
        backend_log.close()
        portal_log.close()


if __name__ == '__main__':
    main()
