# TC07: Vehicle management and compatibility

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Create, edit and delete a vehicle; change its default. Attempt a Type 2 vehicle on a CCS2 bay and a CCS2 vehicle on Type 2 AC.

Exact commands:

```powershell
python run.py
python mobile-vehicles.py
```

Expected result: Changes persist with correct ownership/default selection. The incompatible start is rejected; supported compatibility follows backend rules.

Observed result: The API rejected Type 2 on CCS2 DC and accepted CCS2 on AC. Mobile creation/default selection, edit and deletion were saved and re-read through the application; the compatible charging hold was released.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [add-vehicle-form-clean](add-vehicle-form-clean.png)
- [add-vehicle-form](add-vehicle-form.png)
- [vehicle-create-input](vehicle-create-input.png)
- [vehicle-created-default](vehicle-created-default.png)
- [vehicle-delete-confirmation](vehicle-delete-confirmation.png)
- [vehicle-deleted](vehicle-deleted.png)
- [vehicle-edit-form](vehicle-edit-form.png)
- [vehicle-edit-input](vehicle-edit-input.png)
- [vehicle-edited-default](vehicle-edited-default.png)
