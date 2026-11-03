# TC34: Currency matrix and locked settlement

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Run all nine wallet/tariff currency pairs. Change tariff/FX after acceptance, settle and compare original charge, wallet debit and retained receipt.

Exact commands:

```powershell
python run.py
python regression.py
```

Expected result: Settlement uses accepted values. The wallet and CDR retain their own currencies; subsequent updates do not rewrite the historical receipt.

Observed result: All nine wallet/tariff currency pairs retained accepted values despite later tariff and FX changes. Real terminal responses, CDRs, wallet debits and subsequent reads preserve the historical charge.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
