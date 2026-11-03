# TC44: Persistent migration and seed safety

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Use a disposable legacy fixture containing completed sessions and ledger records. Apply ordered migrations twice, then compare stored values and inventory IDs.

Exact commands:

```powershell
python run.py
```

Expected result: Historical financial values and custom names survive; seeds/migrations do not duplicate the regional inventory.

Observed result: Raw before/after snapshots preserve wallet 54.45, historical charge 31.05, CDR amounts and the custom station name. First-pass regional inventory expansion did not duplicate IDs on the second pass; original seed-idempotency checks also passed.

Status: Done.

Verdict: Passed.

Evidence:

- [migration-before-and-after.txt](migration-before-and-after.txt)
