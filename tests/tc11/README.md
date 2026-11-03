# TC11: History and receipt reconciliation

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Finish a positive-energy session. Open its activity entry and receipt, copy the receipt, and compare its ledger and operator CDR.

Exact commands:

```powershell
python run.py
python mobile-history.py
python regression.py
```

Expected result: Wallet payment, original amount, currencies, accepted FX and identifiers reconcile. Missing paid information stays unknown; history pagination retains the record.

Observed result: A fresh ChargeSync receipt retained SGD 0.18 source cost and MYR 0.62 paid at 3.45. History reopened the same receipt, copy and identifiers were captured, and real paginated responses retained separate records. Original unknown-paid/history regressions passed.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
- [activity-history-input](activity-history-input.png)
- [history-receipt-opened](history-receipt-opened.png)
- [receipt-copied](receipt-copied.png)
- [receipt-identifiers](receipt-identifiers.png)
