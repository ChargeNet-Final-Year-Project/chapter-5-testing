# TC06: Combined discovery filters

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Apply country, region, operator, connector and minimum/maximum power filters. Change country, reset and cancel draft filters; select a search result.

Exact commands:

```powershell
python run.py
python regression.py
python android-filters.py
```

Expected result: Results satisfy the active filters; region resets when country changes. Selection opens the intended station and dismisses search results.

Observed result: Real combined country/region/CPO/connector/power requests and negative range requests were captured. Original draft-cancel, country-reset and search-selection regressions passed; Android captures record the visible filter state.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
- [combined-filter-draft](combined-filter-draft.png)
- [country-change-resets-region](country-change-resets-region.png)
- [country-options](country-options.png)
- [filters-input-form](filters-input-form.png)
- [malaysia-penang-selected](malaysia-penang-selected.png)
- [region-options](region-options.png)
