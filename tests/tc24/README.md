# TC24: Session and CDR receivers

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Send a session update and command callback for a known session. Post a CDR twice and attempt a foreign-owner update.

Exact commands:

```powershell
python run.py
python regression.py
```

Expected result: Updates reach the correct session; duplicate CDR delivery preserves one settlement. Foreign-owner access is denied.

Observed result: Own session updates/callbacks succeeded, foreign ones were denied, and duplicate source CDR delivery retained one CDR/debit. Accepted pricing, rather than the supplied source total of 999, determined accounting.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
