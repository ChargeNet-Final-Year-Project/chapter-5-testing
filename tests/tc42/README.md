# TC42: Portal layout and browser compatibility

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Use available Chromium and Firefox at desktop and narrow widths. Check login, overview, ledger, network and admin navigation by keyboard.

Exact commands:

```powershell
python run.py
python firefox.py
```

Expected result: Data, navigation, errors and financial controls remain readable and operable at each recorded viewport.

Observed result: Edge used 1440/390-pixel views and Firefox 158.0.1 used 1440/500-pixel viewports, with readable content and keyboard focus. The narrow Firefox viewport was 500 pixels, matching the browser minimum window width.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [firefox-console.txt](firefox-console.txt)
- [1440-admin](1440-admin.png)
- [1440-credentials](1440-credentials.png)
- [1440-ledger](1440-ledger.png)
- [1440-network](1440-network.png)
- [1440-overview](1440-overview.png)
- [390-admin](390-admin.png)
- [390-credentials](390-credentials.png)
- [390-ledger](390-ledger.png)
- [390-network](390-network.png)
- [390-overview](390-overview.png)
- [firefox-1440-credentials](firefox-1440-credentials.png)
- [firefox-1440-ledger](firefox-1440-ledger.png)
- [firefox-1440-network](firefox-1440-network.png)
- [firefox-1440-overview](firefox-1440-overview.png)
- [firefox-390-credentials](firefox-390-credentials.png)
- [firefox-390-ledger](firefox-390-ledger.png)
- [firefox-390-network](firefox-390-network.png)
- [firefox-390-overview](firefox-390-overview.png)
