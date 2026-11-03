# TC14: Company and network records

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: Edit a disposable company profile, reload it, then inspect that operator network and connector availability.

Exact commands:

```powershell
python run.py
```

Expected result: Profile changes persist and the network view contains only the authorised operator data with API-consistent status.

Observed result: The browser saved a changed company name/colour and retained them after reload. Its network view and fresh API response showed only the controlled operator station and matching connector state.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [company-form-input](company-form-input.png)
- [edited-company-reloaded](edited-company-reloaded.png)
- [operator-network](operator-network.png)
