import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urlparse

REPOSITORY = Path(__file__).resolve().parents[1]
environment = REPOSITORY / '.env'
if environment.exists():
    for line in environment.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip() or line.lstrip().startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        if re.fullmatch(r'[A-Z][A-Z0-9_]*', key.strip()):
            os.environ.setdefault(key.strip(), value.strip().strip('"\''))

TZ = dt.timezone(dt.timedelta(hours=8))
ROOT = Path(os.environ.get('CHARGENET_WORKSPACE', str(REPOSITORY.parent))).resolve()
RUN = Path(os.environ.get('CHARGENET_RUN_DIR', str(REPOSITORY / 'runs' / dt.datetime.now(TZ).strftime('%Y-%m-%d_%H%M%S')))).resolve()
FLUTTER = os.environ.get('FLUTTER_BIN') or shutil.which('flutter.bat') or shutil.which('flutter') or 'flutter'
ADB = os.environ.get('ADB_BIN') or shutil.which('adb') or str(Path(os.environ.get('ANDROID_HOME', Path.home() / 'AppData/Local/Android/Sdk')) / 'platform-tools/adb.exe')
DB_CONTAINER = os.environ.get('CHARGENET_DB_CONTAINER', 'chargenet-testing-postgres')
TEST_DSN = os.environ.get('TEST_DATABASE_URL', '')
RUNTIME_DSN = os.environ.get('DATABASE_URL', '')


def now():
    return dt.datetime.now(TZ).isoformat()


def validate_test_dsn(value):
    parsed = urlparse(value)
    name = parsed.path.lstrip('/')
    if parsed.scheme not in ['postgres', 'postgresql'] or not parsed.hostname:
        raise ValueError('TEST_DATABASE_URL must identify a PostgreSQL test database')
    if name != 'chargenet_test' and not name.startswith('chargenet_test_'):
        raise ValueError('Refusing destructive tests outside chargenet_test or chargenet_test_*')
    return name


def validate_runtime_dsn(value):
    parsed = urlparse(value)
    if parsed.scheme not in ['postgres', 'postgresql'] or parsed.path != '/chargenet_evidence_test':
        raise ValueError('DATABASE_URL must identify the separate chargenet_evidence_test database')
    return parsed.path.lstrip('/')


def clean(value):
    value = re.sub(r'postgres(?:ql)?://[^\s"\']+', '[REDACTED_DSN]', value)
    for key, secret in os.environ.items():
        if secret and len(secret) >= 4 and re.search(r'PASSWORD|TOKEN|SECRET|BANK_ACCOUNT', key):
            value = value.replace(secret, '[REDACTED]')
    return value


def command(argv, cwd=ROOT, output='provenance/setup.log', env=None, timeout=1800):
    started = now()
    try:
        result = subprocess.run([str(a) for a in argv], cwd=cwd, env={**os.environ, **(env or {})}, capture_output=True, timeout=timeout)
        stdout, stderr, code = result.stdout.decode('utf8', 'replace'), result.stderr.decode('utf8', 'replace'), result.returncode
        status = 'completed'
    except subprocess.TimeoutExpired as error:
        stdout = (error.stdout or b'').decode('utf8', 'replace')
        stderr = (error.stderr or b'').decode('utf8', 'replace') + '\nCommand exceeded its configured timeout.'
        code, status = None, 'timed_out'
    except OSError as error:
        stdout, stderr, code, status = '', str(error), None, 'unavailable'
    target = RUN / output
    target.parent.mkdir(parents=True, exist_ok=True)
    error_path = target.with_name(target.stem + '.stderr.log')
    target.write_text(clean(stdout), encoding='utf8')
    error_path.write_text(clean(stderr), encoding='utf8')
    record = dict(command=clean(subprocess.list2cmdline([str(a) for a in argv])), working_directory=str(cwd), started_at=started, finished_at=now(), exit_code=code, runner_status=status, stdout=output, stderr=error_path.relative_to(RUN).as_posix())
    with (RUN / 'provenance/commands.events.jsonl').open('a', encoding='utf8') as file:
        file.write(json.dumps(record) + '\n')
    print(json.dumps(record), flush=True)
    return code, stdout, stderr


for folder in ['provenance', 'build', 'evidence/backend', 'evidence/mobile', 'evidence/portal', 'evidence/integration', 'evidence/requests', 'evidence/reliability', 'evidence/database', 'evidence/performance', 'evidence/captures']:
    (RUN / folder).mkdir(parents=True, exist_ok=True)
