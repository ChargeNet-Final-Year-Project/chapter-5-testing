# TC37: Portal role and tenant boundaries

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Use no cookie, a CPO cookie and a different CPO identity against protected endpoints, CDR details and administrator actions.

Exact commands:

```powershell
python run.py
```

Expected result: Unauthenticated and unauthorised requests fail. One operator cannot read another operator financial records or approve partners.

Observed result: Signed-out requests returned 401, CPO administrator actions 403, and foreign CDR detail 404 while own detail was available. Denied requests did not alter the accounting records.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
