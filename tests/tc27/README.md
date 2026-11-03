# TC27: Concurrent competing starts

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Run two valid estimates concurrently for one driver; then use two different drivers competing for one connector. Release the starts together with a barrier.

Exact commands:

```powershell
python run.py
```

Expected result: Exactly one competing start wins per constraint. The losing request leaves no charge or hold.

Observed result: Barrier-released starts yielded one winner per driver/connector constraint. Losing wallets retained their funds and no hold. Final grouped SQL counted one session/reservation/CDR for each winner.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
