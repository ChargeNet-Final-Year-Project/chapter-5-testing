# TC43: Measured local response and update delay

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: Under a stated local fixture size, collect 30 timed station reads after five warm-ups; separately timestamp start-to-first-telemetry, pushed updates and scheduled reconciliation.

Exact commands:

```powershell
python run.py
python push-and-pull.py
```

Expected result: Report sample count, median, p95, errors and conditions. Treat timing as descriptive unless a justified threshold is agreed before execution.

Observed result: Thirty successful 38-station transfers after five warm-ups measured median 7.571 ms and nearest-rank p95 8.817 ms; first positive SSE was 1141.148 ms. The separate local source measured normal pull at 287.340 seconds and push visibility at 180.311 ms. These measurements describe the local test conditions.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [timing-samples.csv](timing-samples.csv)
- [push-and-pull-console.txt](push-and-pull-console.txt)
