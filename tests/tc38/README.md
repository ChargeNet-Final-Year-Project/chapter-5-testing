# TC38: OCPI token contract

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: Use missing/unknown tokens, used Token A and a valid token naming a different party against module and callback endpoints.

Exact commands:

```powershell
python run.py
```

Expected result: Only the allowed token/party/module combination succeeds; rejected requests leave records unchanged.

Observed result: Missing/unknown/used registration credentials returned 401, and a valid operational token naming another party returned 403. Callback/module denials left stored inventory unchanged.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
