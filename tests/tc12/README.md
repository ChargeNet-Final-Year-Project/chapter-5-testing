# TC12: Partner onboarding and governance

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: Register a disposable CPO, configure the endpoint, verify credentials and inspect pending access. Approve as administrator, then suspend and restore it.

Exact commands:

```powershell
python run.py
```

Expected result: Connection verification and marketplace approval remain separate. Only eligible partners are discoverable; suspension blocks a saved-station start.

Observed result: Browser verification and administrator approval show VERIFIED/PENDING separately from ACTIVE. Approved inventory was visible; suspension hid it and rejected the saved-station start; restoration succeeded.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [admin-approval-input](admin-approval-input.png)
- [admin-approval-result](admin-approval-result.png)
- [verified-approved](verified-approved.png)
- [verified-pending](verified-pending.png)
