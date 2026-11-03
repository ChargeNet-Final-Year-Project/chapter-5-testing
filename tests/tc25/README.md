# TC25: Start eligibility failures

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder.

Procedure: Independently test insufficient balance, unavailable/unknown EVSE, incompatible vehicle and a second active driver session.

Exact commands:

```powershell
python run.py
```

Expected result: Each rejection reports the appropriate error with no unintended session, financial debit or remaining hold.

Observed result: Real requests rejected insufficient funds, unknown EVSE, inoperative bay, Type 2/DC and a second active session. Only the intentional valid prerequisite session existed; cleanup left one CDR/debit and no hold. Disposable SQL fault setup is explicit.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
