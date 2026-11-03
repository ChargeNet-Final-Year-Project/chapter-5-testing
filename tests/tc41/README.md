# TC41: Accessible confirmation and light appearance

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Test keyboard/focus or assistive confirmation alternatives, interrupted dragging, busy controls and onboarding semantics; inspect representative screens in light mode.

Exact commands:

```powershell
python regression.py
python android-confirmation.py
```

Expected result: Confirmation is accessible, cancelled drags submit nothing, duplicate busy actions are prevented and visible screens retain the light theme.

Observed result: The original 15 accessibility/confirmation tests passed. Android captures record the accessible alternative, cancelled-drag state and representative light-theme behavior.

Status: Done.

Verdict: Passed.

Evidence:

- [supplementary-regression.txt](supplementary-regression.txt)

- [Accessible confirmation dialog](accessible-confirmation-dialog.png)
- [Cancelled drag](cancelled-short-drag.png)
- [Busy controls during start](busy-controls-during-real-start.png)
- [Single live session](one-live-session.png)
- [Light theme receipt](receipt-light-theme.png)
- [Application requests and accounting](requests.txt)
