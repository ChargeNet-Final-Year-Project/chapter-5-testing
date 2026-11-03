# TC09: One account across three operators

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Without switching driver accounts, complete discovery, comparison, estimate review, start, live monitoring, stop and receipt for VoltGo/MY, ChargeSync/SG and EcoWatt/TH.

Exact commands:

```powershell
python run.py
python mobile-journey.py
```

Expected result: All three journeys use the same driver ID. Each has positive energy, a confirmed terminal result, a receipt and matching wallet movement.

Observed result: One demo driver completed all three mobile journeys. Receipts reconcile VoltGo MYR 3.54, ChargeSync MYR 1.90 and EcoWatt MYR 17.86 to single CDR/debit records and released holds. Separate curl journeys also completed.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [Batu Kawan-confirmation-dialog](Batu%20Kawan-confirmation-dialog.png)
- [Batu Kawan-connectors](Batu%20Kawan-connectors.png)
- [Batu Kawan-estimate](Batu%20Kawan-estimate.png)
- [Batu Kawan-live](Batu%20Kawan-live.png)
- [Batu Kawan-receipt](Batu%20Kawan-receipt.png)
- [Batu Kawan-search](Batu%20Kawan-search.png)
- [Batu Kawan-stop-confirmation](Batu%20Kawan-stop-confirmation.png)
- [Hat Yai East-confirmation-controls](Hat%20Yai%20East-confirmation-controls.png)
- [Hat Yai East-confirmation-dialog](Hat%20Yai%20East-confirmation-dialog.png)
- [Hat Yai East-connectors](Hat%20Yai%20East-connectors.png)
- [Hat Yai East-estimate](Hat%20Yai%20East-estimate.png)
- [Hat Yai East-live](Hat%20Yai%20East-live.png)
- [Hat Yai East-receipt](Hat%20Yai%20East-receipt.png)
- [Hat Yai East-reopened-live](Hat%20Yai%20East-reopened-live.png)
- [Hat Yai East-search](Hat%20Yai%20East-search.png)
- [Hat Yai East-stop-confirmation](Hat%20Yai%20East-stop-confirmation.png)
- [Marina Bay-confirmation-dialog](Marina%20Bay-confirmation-dialog.png)
- [Marina Bay-connectors](Marina%20Bay-connectors.png)
- [Marina Bay-estimate](Marina%20Bay-estimate.png)
- [Marina Bay-live](Marina%20Bay-live.png)
- [Marina Bay-receipt](Marina%20Bay-receipt.png)
- [Marina Bay-search](Marina%20Bay-search.png)
- [Marina Bay-stop-confirmation](Marina%20Bay-stop-confirmation.png)
