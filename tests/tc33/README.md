# TC33: Pricing revalidation without expiry

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Accept an old unchanged estimate; repeat with a newer same-value FX record, a changed FX value, a changed tariff and a missing rate source.

Exact commands:

```powershell
python run.py
python regression.py
```

Expected result: Age alone does not reject an estimate. Changed financial terms require review; unavailable FX blocks acceptance without consuming the estimate or reserving funds.

Observed result: Old unchanged and newer same-value FX estimates were accepted. Changed tariff/FX returned QUOTE_CHANGED; missing selected FX returned RATE_UNAVAILABLE without accepting the quote or holding funds. Pricing fixtures were restored.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
