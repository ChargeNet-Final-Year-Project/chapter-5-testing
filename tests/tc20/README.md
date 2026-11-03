# TC20: Pull reconciliation after a missed push

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: Change an emulator location/tariff without pushing it. Let scheduled sync run; compare before/after data and timestamps. Also rerun direct sync tests.

Exact commands:

```powershell
python run.py
```

Expected result: Pull recovers the change on the next successful configured cycle. Record measured delay; an accelerated test timer is identified explicitly.

Observed result: The unaccelerated 300-second scheduler recovered a source-only name/price change after 277.743 seconds. No push/direct sync was issued.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
