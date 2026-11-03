# TC10: Minimise and restore charging

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions. Start a long-running session in the app first; this is application state, not a dependency on another case folder.

Procedure: Start a session, minimise the monitor, change tab and reopen it. Background and foreground the application.

Exact commands:

```powershell
python run.py
```

Expected result: Charging retains the same session ID; fresh telemetry returns without a duplicate start or duplicate receipt.

Observed result: Minimise, tab switching and background/foreground retained the active session ID and newer energy. The mini bar showed live charging; no receipt or debit existed while the session remained active.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [activity-during-charge](activity-during-charge.png)
- [before-minimise](before-minimise.png)
- [foreground-restored-session](foreground-restored-session.png)
- [minimised-monitor](minimised-monitor.png)
- [profile-during-charge](profile-during-charge.png)
