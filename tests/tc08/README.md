# TC08: Simulated wallet top up

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Record the starting wallet and ledger. Submit a valid top up, repeat its Idempotency-Key and try an invalid amount/method.

Exact commands:

```powershell
python run.py
python mobile-topup.py
```

Expected result: One successful credit and one balance increase occur for the repeated request. Invalid inputs leave the wallet unchanged.

Observed result: Replay credited one MYR 100 top-up; invalid amount/method requests left the wallet unchanged. A separate actual mobile top-up increased the same demo wallet from MYR 523.54 to MYR 623.54.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [topup-100-input](topup-100-input.png)
- [topup-form](topup-form.png)
- [topup-result](topup-result.png)
- [wallet-before-topup](wallet-before-topup.png)
