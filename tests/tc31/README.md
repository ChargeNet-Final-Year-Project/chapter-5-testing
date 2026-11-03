# TC31: Recovery of an active session

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Persist positive progress, stop the manager without finalisation, create a fresh manager and gateway, and observe recovery. Separately assess a full process restart.

Exact commands:

```powershell
python run.py
python regression.py
```

Expected result: Persisted progress is retained, with a single final settlement and released connector/hold. Recovery covers manager restart and full backend restart with the in-process OCPI emulators.

Observed result: Full backend process death included all three in-process emulators. Recovery retained saved progress and the same session; final accounting was one CDR/debit with released bay/hold.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
