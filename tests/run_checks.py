import argparse
import json
from pathlib import Path
import shutil
from test_support import ROOT, RUN, FLUTTER, TEST_DSN, command, validate_test_dsn


def go_summary(text):
    events = [json.loads(line) for line in text.splitlines() if line.startswith('{')]
    tests = [event for event in events if event.get('Test')]
    return dict(test_events={action: sum(event.get('Action') == action for event in tests) for action in ['pass', 'fail', 'skip']}, top_level_tests={action: sum(event.get('Action') == action and '/' not in event['Test'] for event in tests) for action in ['pass', 'fail', 'skip']}, failed_packages=[event['Package'] for event in events if event.get('Action') == 'fail' and not event.get('Test')])


def run(suite, checkout=None):
    checkout = Path(checkout or ROOT / ('chargenet-' + suite)).resolve()
    npm = shutil.which('npm.cmd') or shutil.which('npm') or 'npm'
    suites = {
        'backend': [(['go', 'version'], 'provenance/go-version.log'), (['go', 'test', '-json', '-count=1', '-p', '1', './...'], 'evidence/backend/backend-tests.events.jsonl'), (['go', 'vet', './...'], 'evidence/backend/static-analysis.log'), (['go', 'build', './...'], 'evidence/backend/build.log')],
        'mobile': [([FLUTTER, '--version'], 'provenance/flutter-version.log'), ([FLUTTER, 'pub', 'get'], 'evidence/mobile/dependencies.log'), ([FLUTTER, 'analyze'], 'evidence/mobile/static-analysis.log'), ([FLUTTER, 'test', '--concurrency=1', '--machine'], 'evidence/mobile/mobile-tests.events.jsonl'), ([FLUTTER, 'build', 'apk', '--debug'], 'evidence/mobile/android-build.log')],
        'portal': [([npm, 'ci'], 'evidence/portal/dependency-installation.log'), ([npm, 'run', 'typecheck'], 'evidence/portal/type-check.log'), ([npm, 'run', 'build'], 'evidence/portal/production-build.log')],
    }
    if suite == 'backend':
        validate_test_dsn(TEST_DSN)
    for argv, output in suites[suite]:
        code, text, _ = command(argv, checkout, output, {'TEST_DATABASE_URL': TEST_DSN} if suite == 'backend' else None)
        if suite == 'backend' and output.endswith('.jsonl') and text:
            summary = go_summary(text)
            (RUN / 'evidence/backend/backend-test-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
            if summary['test_events']['skip'] or summary['failed_packages'] or not summary['test_events']['pass']:
                return 1
        if code != 0:
            return 1
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run regression checks into a new ignored run directory.')
    parser.add_argument('suite', choices=['backend', 'mobile', 'portal'])
    parser.add_argument('--checkout', type=Path)
    arguments = parser.parse_args()
    raise SystemExit(run(arguments.suite, arguments.checkout))
