# TC23: Unreachable or inactive partner

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Make one emulator unreachable, then test synchronization and command handling. Suspend a disposable partner and retry discovery/start.

Exact commands:

```powershell
python run.py
python regression.py
```

Expected result: The failing partner is reported; reachable partners still synchronize. Suspended inventory is hidden and unusable.

Observed result: Command outage returned CPO_UNREACHABLE without a hold; suspension hid inventory and blocked starts. A dead partner base URL failed verification while the other two partners still verified; endpoint/status were restored.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
