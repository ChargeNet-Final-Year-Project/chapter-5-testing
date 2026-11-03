# TC21: Command routing across nine combinations

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Run the existing roaming test through real loopback OCPI HTTP for every operator and MY/SG/TH combination. Correlate target URLs, party, EVSE and session.

Exact commands:

```powershell
python run.py
```

Expected result: All nine combinations use the intended operator; start, telemetry and stop refer to the same session and connector.

Observed result: All nine real REST/OCPI journeys delivered energy and settled against the intended operator. The verbatim server interval correlates emulator command destinations/callbacks with the captured session IDs and accounting.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [service-routing.log](service-routing.log)
