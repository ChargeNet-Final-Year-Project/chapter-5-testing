# TC18: Location normalisation

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Push valid locations and AC/DC connectors, then read database and driver API. Repeat for all emulator profiles using their station countries.

Exact commands:

```powershell
python run.py
```

Expected result: Identifiers, ownership, geographic country, connector standard, rated power and currency mapping are retained consistently.

Observed result: Nine operator/country reads and joined inventory records retain identity, geographic country, connector standard/power and source currency.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
