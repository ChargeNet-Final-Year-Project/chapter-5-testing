# ChargeNet Chapter 5 tests

For the examination, open [tests/CASES.md](tests/CASES.md), find TC01–TC44, and follow its representative evidence link. Each case keeps the procedure, expected outcome, original result and test-code locations.

- `tests/`: Python procedures/helpers and additional Go tests. Original application suites stay in the sibling `chargenet-backend` and `chargenet-mobile` repositories.
- `evidence/`: original screenshots, captured output, responses, SQL and exports. Existing evidence paths are unchanged. `evidence/figures/sources.json` identifies the sources of composite figures.

Run the self-contained Python checks from this directory (Python 3.12; no extra packages):

```text
python -m unittest discover -s tests/unit -v
```

To rerun application suites, configure disposable PostgreSQL/account values in `.env` using `.env.example`, then follow [tests/RUNNING.md](tests/RUNNING.md). The suite commands are:

```text
python tests/run_checks.py backend --checkout .work/backend
python tests/run_checks.py mobile
python tests/run_checks.py portal
```

Prepare `.work/backend` with `python tests/prepare_backend_checkout.py --source ../chargenet-backend` first. Browser/device procedures require the isolated running services, optional `requirements.txt` dependencies and the documented screen/account state. New results go to ignored `runs/`; captured results remain unchanged.

Charging, operators, wallets and FX are simulated. Timing measurements describe the recorded local setup. One representative item does not demonstrate every substep; additional original records are linked in the case catalogue.
