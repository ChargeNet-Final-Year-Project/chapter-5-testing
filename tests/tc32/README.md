# TC32: Recovery of interrupted settlement

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Persist the settlement request, interrupt processing before final accounting, and run a new manager. Repeat recovery once more.

Exact commands:

```powershell
python run.py
python regression.py
```

Expected result: Accepted pricing and stopped energy remain fixed. Recovery creates one debit/CDR and releases the hold without restarting delivery.

Observed result: A recorded disposable settlement intent survived abrupt restart. Fixed energy/accepted pricing produced one debit/CDR, and a second restart preserved those values with no hold.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
