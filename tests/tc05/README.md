# TC05: Station discovery and comparison

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Use one account to find VoltGo, ChargeSync and EcoWatt. Compare available MY, SG and TH stations and open connector details.

Exact commands:

```powershell
python run.py
python mobile-discovery.py
```

Expected result: Operator, country, connector, AC/DC power, availability and source-currency price agree with the API.

Observed result: Real search and connector views show VoltGo/MY, ChargeSync/SG and EcoWatt/TH with the source-country price, power and availability. Driver responses and SQL inventory accompany those screens.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [chargesync-search-input-and-results](chargesync-search-input-and-results.png)
- [chargesync-station-and-connectors](chargesync-station-and-connectors.png)
- [ecowatt-search-input-and-results](ecowatt-search-input-and-results.png)
- [ecowatt-station-and-connectors](ecowatt-station-and-connectors.png)
- [voltgo-search-input-and-results](voltgo-search-input-and-results.png)
- [voltgo-station-and-connectors](voltgo-station-and-connectors.png)
