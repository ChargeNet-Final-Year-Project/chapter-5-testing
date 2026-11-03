# TC39: Login throttling and session expiry

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Repeat incorrect portal login until the configured threshold is reached, then test an expired session and logout in the browser.

Exact commands:

```powershell
python run.py
```

Expected result: Configured login throttling returns the expected rate-limit response. Expired/logout state removes protected access and stale account views.

Observed result: Five invalid logins returned 401, then rate limiting returned 429. A correctly signed expired JWT and signed-out protected navigation each returned the actual browser to login.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [expired-session-rejected](expired-session-rejected.png)
- [signed-out-protected-navigation](signed-out-protected-navigation.png)
