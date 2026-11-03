# TC28: Repeated stop and concurrent settlement

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Charge positive energy, stop, repeat stop and invoke competing settlement attempts. Compare CDR and debit counts before and after.

Exact commands:

```powershell
python run.py
```

Expected result: One CDR and one positive wallet debit remain, with unchanged final amount and no remaining hold. Connector becomes available.

Observed result: Concurrent and repeated stops returned the same final charge/CDR. SQL retained one positive debit, one CDR, no hold and an AVAILABLE bay.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
