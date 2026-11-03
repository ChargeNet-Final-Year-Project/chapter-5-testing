# TC16: Sandbox trace and revenue exclusion

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Record operator totals. Run sandbox start/stop, inspect the accepted response and later observation, then log out and recheck totals.

Exact commands:

```powershell
python run.py
```

Expected result: Sandbox trace distinguishes acknowledgement from later state; logout clears it. Sandbox records are excluded from operator revenue.

Observed result: The actual sandbox trace distinguished ACCEPTED from later OBSERVED status changes. Non-sandbox currency totals stayed unchanged, and signing out/back in displayed an empty trace.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [history-cleared-after-signout](history-cleared-after-signout.png)
- [start-accepted-and-observed](start-accepted-and-observed.png)
- [start-command-input](start-command-input.png)
- [stop-accepted-and-observed](stop-accepted-and-observed.png)
