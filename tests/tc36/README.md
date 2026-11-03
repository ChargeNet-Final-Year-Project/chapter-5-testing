# TC36: Driver ownership boundaries

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: As a second driver, request another driver vehicle, estimate, session, stream and history identifiers through direct API calls.

Exact commands:

```powershell
python run.py
```

Expected result: No private record or financial action is exposed. Record exact denial status and verify unchanged stored data.

Observed result: A funded second driver could not access/edit/delete the owner's records or use its estimate. Direct denials and unchanged before/after records/accounting are retained; the second history remained private.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
