# TC35: Automatic stop and zero cost boundary

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Run target reached and balance exhausted cases; stop a zero-energy session. Inspect wallet liability fields and repeat settlement.

Exact commands:

```powershell
python run.py
python regression.py
```

Expected result: Automatic stops preserve valid terminal state. Debit never exceeds available funds; any unfunded amount is traceable. Zero energy creates no positive debit or duplicate record.

Observed result: An already-reached target created one zero-value CDR without a debit. Balance exhaustion charged MYR 9.98 from MYR 10, leaving MYR 0.02 and zero hold. Repeated settlement and original boundary regressions passed.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
