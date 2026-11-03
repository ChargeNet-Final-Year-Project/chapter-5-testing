# TC04: Driver account access

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Register a test account, sign in, reopen the application and sign out. Try invalid credentials and a duplicate email.

Exact commands:

```powershell
python run.py
python mobile-access.py
python mobile-account.py
python mobile-register.py
python mobile-duplicate.py
```

Expected result: Valid access restores the correct account. Invalid input receives an error; logout clears account data.

Observed result: The actual app rejected wrong credentials and duplicate registration, registered a new driver, restored the same account after reopening, and returned to the login gate on sign-out. API denials independently returned 401/409.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [after-onboarding](after-onboarding.png)
- [app-after-idle](app-after-idle.png)
- [demo-restored-for-next-cases](demo-restored-for-next-cases.png)
- [duplicate-registration-input](duplicate-registration-input.png)
- [duplicate-registration-result](duplicate-registration-result.png)
- [emulator-after-cold-start](emulator-after-cold-start.png)
- [emulator-initial](emulator-initial.png)
- [invalid-login-input](invalid-login-input.png)
- [invalid-login-result](invalid-login-result.png)
- [onboarding-next](onboarding-next.png)
- [recovered-app-screen](recovered-app-screen.png)
- [registered-profile-after-reopen](registered-profile-after-reopen.png)
- [registered-profile](registered-profile.png)
- [registration-form](registration-form.png)
- [registration-input](registration-input.png)
- [registration-result](registration-result.png)
- [restored-profile](restored-profile.png)
- [signed-out-login](signed-out-login.png)
- [valid-login-input](valid-login-input.png)
- [valid-login-result](valid-login-result.png)
