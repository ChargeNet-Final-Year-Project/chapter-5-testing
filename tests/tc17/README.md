# TC17: Version and credential exchange

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Port 18090 must be free; this case includes its complete controlled source.

Procedure: Exercise discovery, implemented module details, Token A registration, token rotation and unregistration on a disposable partner.

Exact commands:

```powershell
python run.py
```

Expected result: The implemented 2.3.0 surface is advertised; token lifecycle and module permissions match the tested contract.

Observed result: Real version/module discovery, used-A denial, operational rotation, old-token denial and unregistration followed the token contract. The final profile has cleared credentials and SUSPENDED status.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
