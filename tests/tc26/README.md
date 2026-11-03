# TC26: Repeated start response

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Start with an Idempotency-Key and repeat the identical request, including a replay after a deliberately lost response. Compare IDs and database rows.

Exact commands:

```powershell
python run.py
```

Expected result: The original session is returned with replay evidence; only one session and reservation exist.

Observed result: A complete socket start committed before its unread response was discarded. Curl replay returned the original ID and replay header. SQL counted one session, reservation and CDR; completion left one debit and zero hold.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
