# TC19: Status and tariff push

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: Snapshot an isolated connector and tariff. Apply a valid status patch and tariff update; reload driver and portal data.

Exact commands:

```powershell
python run.py
```

Expected result: The updated availability and price reach storage and consumer APIs without changing partner ownership. Restore the fixture.

Observed result: Real tariff/location pushes changed the connector to INOPERATIVE and MYR 1.75 without changing CPO ownership. Driver/portal responses and SQL show the result; the original fixture was restored.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
