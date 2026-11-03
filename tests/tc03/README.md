# TC03: Portal build baseline

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Install from package-lock.json. Run the TypeScript check and production build.

Exact commands:

```powershell
python run.py
```

Expected result: Both commands succeed.

Observed result: The locked npm installation, TypeScript check and production build exited 0 at the final report revision.

Status: Done.

Verdict: Passed.

Evidence:

- [portal-build-full.txt](portal-build-full.txt)
