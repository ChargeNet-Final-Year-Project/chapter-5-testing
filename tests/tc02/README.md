# TC02: Mobile regression baseline

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Resolve the locked dependencies with the documented Flutter toolchain. Run analysis and all Flutter tests with concurrency one.

Exact commands:

```powershell
python run.py
```

Expected result: Analysis and tests complete successfully. Retain machine-readable test events and actual totals.

Observed result: Locked dependencies, analysis, all 265 Flutter tests and the Android debug APK build passed.

Status: Done.

Verdict: Passed.

Evidence:

- [mobile-regression-full.txt](mobile-regression-full.txt)
