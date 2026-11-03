# TC15: Revenue currencies and full export

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Create more matching records than one visible page. Select each currency and a date range around Kuala Lumpur midnight; compare overview, ledger and CSV.

Exact commands:

```powershell
python run.py
```

Expected result: Totals use one currency and settlement dates in Asia/Kuala_Lumpur. CSV contains the complete matching range and agrees with database totals.

Observed result: Records dated 1 November verify the Kuala Lumpur boundary: 26 records per currency, 25+1 JSON pagination and complete CSVs. Each currency has 41.60 gross, 2.08 fee and 39.52 net matching SQL. Separate currency overview totals were captured.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [MYR-ledger](MYR-ledger.png)
- [MYR-overview](MYR-overview.png)
- [overview](overview.png)
- [SGD-ledger](SGD-ledger.png)
- [SGD-overview](SGD-overview.png)
- [THB-ledger](THB-ledger.png)
- [THB-overview](THB-overview.png)
- [MYR-browser-export.csv](MYR-browser-export.csv)
- [MYR-full-export.csv](MYR-full-export.csv)
- [SGD-browser-export.csv](SGD-browser-export.csv)
- [SGD-full-export.csv](SGD-full-export.csv)
- [THB-browser-export.csv](THB-browser-export.csv)
- [THB-full-export.csv](THB-full-export.csv)
