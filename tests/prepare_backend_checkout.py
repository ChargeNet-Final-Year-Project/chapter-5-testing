import argparse
from pathlib import Path
import shutil
import subprocess
from test_support import REPOSITORY

RECORDED_COMMIT = 'ca5052217633bb405ceb52f5e98e9b61ccd060ba'


def prepare(source, destination, commit=RECORDED_COMMIT):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.exists():
        raise ValueError('Destination already exists; use a new isolated checkout path')
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', '-c', 'safe.directory=' + source.as_posix(), 'clone', '--no-hardlinks', '--no-checkout', str(source), str(destination)], check=True)
    subprocess.run(['git', '-C', str(destination), 'config', 'core.autocrlf', 'false'], check=True)
    subprocess.run(['git', '-C', str(destination), 'checkout', '--detach', commit], check=True)
    for test in (REPOSITORY / 'tests/backend').rglob('*_test.go'):
        target = destination / test.relative_to(REPOSITORY / 'tests/backend')
        if target.exists() and target.read_bytes() != test.read_bytes():
            raise ValueError('Existing test differs from the recorded test snapshot: ' + str(target))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(test, target)
    print('Prepared backend checkout at ' + str(destination))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare an isolated backend checkout with the recorded additional tests.')
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--destination', type=Path, default=REPOSITORY / '.work/backend')
    parser.add_argument('--commit', default=RECORDED_COMMIT)
    arguments = parser.parse_args()
    prepare(arguments.source, arguments.destination, arguments.commit)
