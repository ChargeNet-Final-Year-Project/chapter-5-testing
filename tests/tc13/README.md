# TC13: Credential display and disconnect

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: As a disposable operator, reveal/copy unused Token A, complete the exchange, inspect masked operational hints, then disconnect.

Exact commands:

```powershell
python run.py
```

Expected result: Token A becomes unusable after exchange; full B/C values are absent from browser responses. Disconnect changes integration state. Capture only redacted evidence.

Observed result: The browser revealed, copied and hid unused Token A. Used A was rejected, B/C full values were absent from the portal response, and operational disconnect cleared tokens and suspended the approved partner.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [consumed-token-masked](consumed-token-masked.png)
- [disconnected](disconnected.png)
- [unused-token-hidden](unused-token-hidden.png)
- [unused-token-masked](unused-token-masked.png)
- [unused-token-revealed](unused-token-revealed.png)
