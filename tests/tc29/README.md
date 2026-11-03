# TC29: Stop timeout and uncertain completion

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Interrupt the stop callback or terminal update. Observe the timeout and mobile reconciliation; later deliver authoritative terminal state.

Exact commands:

```powershell
python run.py
python android-uncertainty.py
python regression.py
```

Expected result: The interface preserves uncertainty until confirmation; no premature receipt or duplicate settlement appears. Recovery produces the correct final record.

Observed result: Three unconfirmed stops left CHARGING, held funds and zero CDR/debit. The actual app displayed uncertainty. An authoritative terminal update produced one receipt/settlement; later retries and emulator cleanup did not duplicate it.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
- [authoritative-completion-receipt](authoritative-completion-receipt.png)
- [live-before-unconfirmed-stop](live-before-unconfirmed-stop.png)
- [stop-confirmation-input](stop-confirmation-input.png)
- [unconfirmed-stop-remains-active](unconfirmed-stop-remains-active.png)
