# TC30: Telemetry interruption and reconnection

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Interrupt SSE while charging, keep REST available, then interrupt all connectivity. Restore it and deliver an old frame after a newer snapshot.

Exact commands:

```powershell
python run.py
python regression.py
```

Expected result: Polling/reconnection restores the same session. Missing data is shown as uncertain; stale responses do not overwrite a newer session or cause a receipt.

Observed result: The real forwarding proxy interrupted SSE while REST continued. Full network loss displayed uncertainty; explicit retry restored fresh same-session readings. A captured genuine old frame was replayed after newer state without replacing it; final accounting stayed singular.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
- [after-old-frame-replay](after-old-frame-replay.png)
- [all-connectivity-lost](all-connectivity-lost.png)
- [confirmed-completion-after-recovery](confirmed-completion-after-recovery.png)
- [connectivity-restored](connectivity-restored.png)
- [live-before-loss](live-before-loss.png)
- [network-restored-before-explicit-retry](network-restored-before-explicit-retry.png)
- [sse-only-interruption-rest-available](sse-only-interruption-rest-available.png)
