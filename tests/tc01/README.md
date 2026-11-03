# TC01: Backend regression baseline

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Start an isolated PostgreSQL 16 test service. Run the complete uncached Go suite serially, then vet and build. Inspect every skip.

Exact commands:

```powershell
python run.py
```

Expected result: Database suites execute; all required assertions, vet and build succeed. Record failures and skips separately.

Observed result: 133 top-level Go tests passed without failures or skips at the final report revision. Vet and build exited 0; the original additional safety checks ran with the suite.

Status: Done.

Verdict: Passed.

Evidence:

- [backend-regression-full.txt](backend-regression-full.txt)
