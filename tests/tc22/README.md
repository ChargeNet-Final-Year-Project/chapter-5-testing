# TC22: Malformed and foreign partner data

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: Submit malformed locations/tariffs, contradictory IDs and another partner identity with an otherwise valid token.

Exact commands:

```powershell
python run.py
```

Expected result: Requests receive the implemented validation/authentication error and do not alter another partner records.

Observed result: Malformed/contradictory data returned 400; a valid token targeting the existing VoltGo identity returned 403. Before/after VoltGo and controlled-partner responses stayed unchanged.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
