# Chapter 5 cases

Find a test ID here, read its procedure and expected result, then open its representative evidence. Paths in the report are relative to this repository. A representative item shows one outcome; the supporting records cover additional steps.

Application test paths below are relative to the sibling backend/mobile/portal repositories. Additional Go tests live in `backend/`; Python procedures live alongside this file. [Running the tests](RUNNING.md). Original captured results are retained; a rerun writes to `runs/`.

## TC01: Backend regression baseline

Procedure: Start an isolated PostgreSQL 16 test service. Run the complete uncached Go suite serially, then vet and build. Inspect every skip.

Expected: Database suites execute; all required assertions, vet and build succeed. Record failures and skips separately.

Captured result (Pass): The complete current serial backend run passed 222 test/subtest events across 133 top-level tests, with zero test failures or skipped tests. Static analysis and build both exited 0.

Test code: backend: [Makefile](../../chargenet-backend/Makefile); [docs/TESTING.md](../../chargenet-backend/docs/TESTING.md); [internal/testutil/db.go](../../chargenet-backend/internal/testutil/db.go).

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

Supporting records: [backend-test-summary.json](../evidence/backend/backend-test-summary.json), [static-analysis.log](../evidence/backend/static-analysis.log), [build.log](../evidence/backend/build.log).

## TC02: Mobile regression baseline

Procedure: Resolve the locked dependencies with the documented Flutter toolchain. Run analysis and all Flutter tests with concurrency one.

Expected: Analysis and tests complete successfully. Retain machine-readable test events and actual totals.

Captured result (Pass): Flutter 3.47.1/Dart 3.13.1 resolved dependencies, passed analysis and completed 265 visible tests with no failures or skips. A further 33 hidden runner/setup events completed. The Android debug APK built successfully.

Test code: mobile: [pubspec.yaml](../../chargenet-mobile/pubspec.yaml); [test/](../../chargenet-mobile/test/).

Representative evidence: [evidence/mobile/mobile-tests.log](../evidence/mobile/mobile-tests.log)

Supporting records: [mobile-test-summary.json](../evidence/mobile/mobile-test-summary.json), [static-analysis.log](../evidence/mobile/static-analysis.log), [android-build.log](../evidence/mobile/android-build.log).

## TC03: Portal build baseline

Procedure: Install from package-lock.json. Run the TypeScript check and production build.

Expected: Both commands succeed. Build success establishes compilation only.

Captured result (Pass): Dependency installation, TypeScript checking and production build passed in the recorded successful run. The restored original checkout also passed type checking and build.

Test code: portal: [package.json](../../chargenet-portal/package.json); [package-lock.json](../../chargenet-portal/package-lock.json).

Representative evidence: [evidence/portal/production-build.log](../evidence/portal/production-build.log)

Supporting records: [dependency-installation.log](../evidence/portal/dependency-installation.log), [type-check.log](../evidence/portal/type-check.log).

## TC04: Driver account access

Procedure: Register a test account, sign in, reopen the application and sign out. Try invalid credentials and a duplicate email.

Expected: Valid access restores the correct account. Invalid input receives an error; logout clears account data.

Captured result (Pass): API and Flutter access tests passed, including invalid/duplicate-account cases. The Android app restored the demo account after cold restarts; sign-out returned to the login gate.

Test code: backend: [internal/api/auth_handler_test.go](../../chargenet-backend/internal/api/auth_handler_test.go); mobile: [test/auth_test.dart](../../chargenet-mobile/test/auth_test.dart); [test/api_service_test.dart](../../chargenet-mobile/test/api_service_test.dart).

Representative evidence: [evidence/mobile/tc04-logout.json](../evidence/mobile/tc04-logout.json)

Supporting records: [tc04-restored-profile.json](../evidence/mobile/tc04-restored-profile.json), [backend-tests.log](../evidence/backend/backend-tests.log), [mobile-tests.log](../evidence/mobile/mobile-tests.log).

## TC05: Station discovery and comparison

Procedure: Use one account to find VoltGo, ChargeSync and EcoWatt. Compare available MY, SG and TH stations and open connector details.

Expected: Operator, country, connector, AC/DC power, availability and source-currency price agree with the API.

Captured result (Pass): Android discovery and connector views were captured for VoltGo Batu Kawan/MY, ChargeSync Marina Bay/SG and EcoWatt Hat Yai East/TH. Operator, connector power and source tariffs correlate with their recorded API journeys.

Test code: backend: [internal/api/station_handler_test.go](../../chargenet-backend/internal/api/station_handler_test.go); mobile: [test/models_test.dart](../../chargenet-mobile/test/models_test.dart); [test/connector_tile_test.dart](../../chargenet-mobile/test/connector_tile_test.dart).

Representative evidence: [evidence/captures/android-tc05-chargesync-discovery.png](../evidence/captures/android-tc05-chargesync-discovery.png)

Supporting records: [demo-roaming-results.json](../evidence/integration/demo-roaming-results.json).

## TC06: Combined discovery filters

Procedure: Apply country, region, operator, connector and minimum/maximum power filters. Change country, reset and cancel draft filters; select a search result.

Expected: Results satisfy the active filters; region resets when country changes. Selection opens the intended station and dismisses search results.

Captured result (Pass): Backend and Flutter filter/controller/search-selection tests passed. Android country selections and search-result opening were exercised for MY, SG and TH; the selected station opened and search results dismissed.

Test code: backend: [internal/api/station_filters_test.go](../../chargenet-backend/internal/api/station_filters_test.go); mobile: [test/station_filters_test.dart](../../chargenet-mobile/test/station_filters_test.dart); [test/discovery_controller_test.dart](../../chargenet-mobile/test/discovery_controller_test.dart); [test/home_search_selection_test.dart](../../chargenet-mobile/test/home_search_selection_test.dart).

Representative evidence: [evidence/mobile/mobile-tests.log](../evidence/mobile/mobile-tests.log)

Supporting records: [backend-tests.log](../evidence/backend/backend-tests.log).

For suite logs, search for the test name above; the following PASS line records its result.

## TC07: Vehicle management and compatibility

Procedure: Create, edit and delete a vehicle; change its default. Attempt a Type 2 vehicle on a CCS2 bay and a CCS2 vehicle on Type 2 AC.

Expected: Changes persist with correct ownership/default selection. The incompatible start is rejected; supported compatibility follows backend rules.

Captured result (Pass): Vehicle API ownership/default/CRUD tests, compatibility validation and the Flutter vehicle-edit tests passed. Incompatible Type 2/DC and supported CCS2/AC rules were exercised by the backend validation tests.

Test code: backend: [internal/api/vehicle_handler_test.go](../../chargenet-backend/internal/api/vehicle_handler_test.go); [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestStartValidationOrder; mobile: [test/vehicle_edit_test.dart](../../chargenet-mobile/test/vehicle_edit_test.dart).

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

Supporting records: [mobile-tests.log](../evidence/mobile/mobile-tests.log).

For suite logs, search for the test name above; the following PASS line records its result.

## TC08: Simulated wallet top up

Procedure: Record the starting wallet and ledger. Submit a valid top up, repeat its Idempotency-Key and try an invalid amount/method.

Expected: One successful credit and one balance increase occur for the repeated request. Invalid inputs leave the wallet unchanged.

Captured result (Pass): Wallet API tests verified replayed top-ups and invalid input. A genuine Android top-up increased the same driver wallet by exactly MYR 100; the before/after API balances are retained.

Test code: backend: [internal/api/wallet_handler_test.go](../../chargenet-backend/internal/api/wallet_handler_test.go); mobile: [test/topup_sheet_test.dart](../../chargenet-mobile/test/topup_sheet_test.dart); [test/wallet_card_test.dart](../../chargenet-mobile/test/wallet_card_test.dart).

Representative evidence: [evidence/integration/tc08-mobile-topup-success.json](../evidence/integration/tc08-mobile-topup-success.json)

Supporting records: [backend-tests.log](../evidence/backend/backend-tests.log), [mobile-tests.log](../evidence/mobile/mobile-tests.log).

## TC09: One account across three operators

Procedure: Without switching driver accounts, complete discovery, comparison, estimate review, start, live monitoring, stop and receipt for VoltGo/MY, ChargeSync/SG and EcoWatt/TH.

Expected: All three journeys use the same driver ID. Each has positive energy, a confirmed terminal result, a receipt and matching wallet movement.

Captured result (Pass): The same driver completed all three Android journeys, including discovery, estimate, live monitoring, stop and receipt. Every journey delivered positive energy and reconciled its original charge, MYR debit and released hold. The existing HTTP demo also passed separately.

Test code: backend: [scripts/demo_roaming.py](../../chargenet-backend/scripts/demo_roaming.py); [internal/api/roaming_e2e_test.go](../../chargenet-backend/internal/api/roaming_e2e_test.go); mobile: [test/active_charging_test.dart](../../chargenet-mobile/test/active_charging_test.dart); [test/charging_receipt_test.dart](../../chargenet-mobile/test/charging_receipt_test.dart).

Representative evidence: [evidence/captures/android-tc11-chargesync-receipt-details.png](../evidence/captures/android-tc11-chargesync-receipt-details.png)

Supporting records: [tc09-mobile-voltgo.json](../evidence/integration/tc09-mobile-voltgo.json), [tc09-mobile-chargesync-journey.json](../evidence/integration/tc09-mobile-chargesync-journey.json), [tc09-mobile-ecowatt-journey.json](../evidence/integration/tc09-mobile-ecowatt-journey.json), [accounting-checks.json](../evidence/database/accounting-checks.json).

## TC10: Minimise and restore charging

Procedure: Start a session, minimise the monitor, change tab and reopen it. Background and foreground the application.

Expected: Charging retains the same session ID; fresh telemetry returns without a duplicate start or duplicate receipt.

Captured result (Pass): The VoltGo session remained the same through minimise, tab change and Android background/foreground. Restored monitoring showed later telemetry; one final settlement remained. Coordinator and mini-bar widget tests also passed.

Test code: mobile: [test/session_coordinator_test.dart](../../chargenet-mobile/test/session_coordinator_test.dart); [test/active_charging_test.dart](../../chargenet-mobile/test/active_charging_test.dart); [test/charging_mini_bar_test.dart](../../chargenet-mobile/test/charging_mini_bar_test.dart).

Representative evidence: [evidence/mobile/mobile-tests.log](../evidence/mobile/mobile-tests.log)

Supporting records: [tc09-mobile-voltgo-active.json](../evidence/integration/tc09-mobile-voltgo-active.json), [tc10-android-restored.json](../evidence/integration/tc10-android-restored.json), [accounting-checks.json](../evidence/database/accounting-checks.json).

For suite logs, search for the test name above; the following PASS line records its result.

## TC11: History and receipt reconciliation

Procedure: Finish a positive-energy session. Open its activity entry and receipt, copy the receipt, and compare its ledger and operator CDR.

Expected: Wallet payment, original amount, currencies, accepted FX and identifiers reconcile. Missing paid information stays unknown; history pagination retains the record.

Captured result (Pass): Actual Android receipts were opened and copied. Their original amounts, accepted rates, wallet payments and CDRs reconcile with the exported database rows. History/receipt/pagination widget tests passed.

Test code: mobile: [test/activity_screen_test.dart](../../chargenet-mobile/test/activity_screen_test.dart); [test/charging_receipt_test.dart](../../chargenet-mobile/test/charging_receipt_test.dart); [test/multi_currency_test.dart](../../chargenet-mobile/test/multi_currency_test.dart); backend: [internal/api/roaming_e2e_test.go](../../chargenet-backend/internal/api/roaming_e2e_test.go).

Representative evidence: [evidence/captures/android-tc11-chargesync-receipt-details.png](../evidence/captures/android-tc11-chargesync-receipt-details.png)

Supporting records: [tc09-mobile-chargesync-journey.json](../evidence/integration/tc09-mobile-chargesync-journey.json), [tc09-mobile-ecowatt-journey.json](../evidence/integration/tc09-mobile-ecowatt-journey.json), [session-cdr-wallet.csv](../evidence/database/session-cdr-wallet.csv), [mobile-tests.log](../evidence/mobile/mobile-tests.log).

## TC12: Partner onboarding and governance

Procedure: Register a disposable CPO, configure the endpoint, verify credentials and inspect pending access. Approve as administrator, then suspend and restore it.

Expected: Connection verification and marketplace approval remain separate. Only eligible partners are discoverable; suspension blocks a saved-station start.

Captured result (Pass): A disposable partner was VERIFIED while still PENDING and absent from driver discovery. Administrator activation exposed its station; suspension hid it and rejected a saved-station start. Activation was restored, and both governance states were captured.

Test code: backend: [internal/api/portal_test.go](../../chargenet-backend/internal/api/portal_test.go) TestPortalRegisterProfileAndHandshake and TestPortalAdminConsoleAndTenancy; [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestStartRejectsSuspendedCpo; portal: [src/pages/Admin.tsx](../../chargenet-portal/src/pages/Admin.tsx).

Representative evidence: [evidence/captures/edge-tc12-verified-approved.png](../evidence/captures/edge-tc12-verified-approved.png)

Supporting records: [tc12-governance.json](../evidence/integration/tc12-governance.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC13: Credential display and disconnect

Procedure: As a disposable operator, reveal/copy unused Token A, complete the exchange, inspect masked operational hints, then disconnect.

Expected: Token A becomes unusable after exchange; full B/C values are absent from browser responses. Disconnect changes integration state. Capture only redacted evidence.

Captured result (Pass): An unused Token A was revealed, copied, compared in memory and hidden without retaining its value. Full operational B/C values were absent from the actual profile response. Consumed Token A and rotated Token C were denied; unregistration cleared integration credentials.

Test code: backend: [internal/api/portal_test.go](../../chargenet-backend/internal/api/portal_test.go) TestPortalDisconnectCredentials; [internal/ocpi/ocpi_test.go](../../chargenet-backend/internal/ocpi/ocpi_test.go); portal: [src/pages/Credentials.tsx](../../chargenet-portal/src/pages/Credentials.tsx).

Representative evidence: [evidence/integration/tc17-tc13-token-lifecycle.json](../evidence/integration/tc17-tc13-token-lifecycle.json)

Supporting records: [browser-checks.json](../evidence/portal/browser-checks.json), [tc13-operational-token-payload-check.json](../evidence/integration/tc13-operational-token-payload-check.json).

## TC14: Company and network records

Procedure: Edit a disposable company profile, reload it, then inspect that operator network and connector availability.

Expected: Profile changes persist and the network view contains only the authorised operator data with API-consistent status.

Captured result (Pass): A disposable company name was updated through HTTP and verified after a full browser reload. Real operator network navigation was exercised; tenant-scoped server tests passed. Banking values were excluded from captures and traces.

Test code: backend: [internal/api/portal_test.go](../../chargenet-backend/internal/api/portal_test.go); portal: [src/pages/Company.tsx](../../chargenet-portal/src/pages/Company.tsx); [src/pages/Network.tsx](../../chargenet-portal/src/pages/Network.tsx).

Representative evidence: [evidence/integration/tc14-profile-reload.json](../evidence/integration/tc14-profile-reload.json)

Supporting records: [browser-results.json](../evidence/portal/browser-results.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC15: Revenue currencies and full export

Procedure: Create more matching records than one visible page. Select each currency and a date range around Kuala Lumpur midnight; compare overview, ledger and CSV.

Expected: Totals use one currency and settlement dates in Asia/Kuala_Lumpur. CSV contains the complete matching range and agrees with database totals.

Captured result (Pass): For each of MYR, SGD and THB, 26 synthetic report records occupied pages of 25 and 1. Each complete CSV contained 26 matching records, gross 41.60 and net 39.52 in that source currency, matching SQL. Midnight-outside and sandbox fixtures were excluded.

Test code: backend: [internal/api/portal_reporting_test.go](../../chargenet-backend/internal/api/portal_reporting_test.go); [internal/api/reporting_range_test.go](../../chargenet-backend/internal/api/reporting_range_test.go); portal: [src/pages/Ledger.tsx](../../chargenet-portal/src/pages/Ledger.tsx); [src/ui/reporting.ts](../../chargenet-portal/src/ui/reporting.ts).

Representative evidence: [evidence/captures/edge-tc15-full-range-myr.png](../evidence/captures/edge-tc15-full-range-myr.png)

Supporting records: [tc15-currency-midnight-pagination.json](../evidence/integration/tc15-currency-midnight-pagination.json), [tc15-totals-myr.csv](../evidence/database/tc15-totals-myr.csv), [tc15-totals-sgd.csv](../evidence/database/tc15-totals-sgd.csv), [tc15-totals-thb.csv](../evidence/database/tc15-totals-thb.csv), [browser-checks.json](../evidence/portal/browser-checks.json).

## TC16: Sandbox trace and revenue exclusion

Procedure: Record operator totals. Run sandbox start/stop, inspect the accepted response and later observation, then log out and recheck totals.

Expected: Sandbox trace distinguishes acknowledgement from later state; logout clears it. Sandbox records are excluded from operator revenue.

Captured result (Pass): The browser sandbox request was accepted on an available connector and the later network state was observed. The retained totals check confirms that sandbox records are excluded from operator revenue.

Test code: backend: [internal/api/portal_test.go](../../chargenet-backend/internal/api/portal_test.go); portal: [src/pages/Sandbox.tsx](../../chargenet-portal/src/pages/Sandbox.tsx); [src/ui/sandboxTrace.ts](../../chargenet-portal/src/ui/sandboxTrace.ts).

Representative evidence: [evidence/captures/edge-tc16-sandbox-stop.png](../evidence/captures/edge-tc16-sandbox-stop.png)

Supporting records: [browser-workflow-results.json](../evidence/portal/browser-workflow-results.json), [tc16-sandbox-browser-trace.json](../evidence/integration/tc16-sandbox-browser-trace.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC17: Version and credential exchange

Procedure: Exercise discovery, implemented module details, Token A registration, token rotation and unregistration on a disposable partner.

Expected: The implemented 2.3.0 surface is advertised; token lifecycle and module permissions match the tested contract.

Captured result (Pass): The live receiver advertised 2.3.0 plus 2.2.1 compatibility. Discovery, module directions, credential exchange, consumed-token denial, rotation and unregistration were exercised. The protocol conclusion covers the implemented subset.

Test code: backend: [internal/ocpi/ocpi_test.go](../../chargenet-backend/internal/ocpi/ocpi_test.go); internal/ocpi/version_test.go; [internal/ocpi/emulator/emulator_test.go](../../chargenet-backend/internal/ocpi/emulator/emulator_test.go) TestEmulatorRegistersWithChargeNet.

Representative evidence: [evidence/integration/tc17-tc13-token-lifecycle.json](../evidence/integration/tc17-tc13-token-lifecycle.json)

Supporting records: [tc17-versions.json](../evidence/integration/tc17-versions.json), [tc17-modules.json](../evidence/integration/tc17-modules.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC18: Location normalisation

Procedure: Push valid locations and AC/DC connectors, then read database and driver API. Repeat for all emulator profiles using their station countries.

Expected: Identifiers, ownership, geographic country, connector standard, rated power and currency mapping are retained consistently.

Captured result (Pass): Receiver normalization tests and all nine real-loopback operator/country journeys passed. Stations retained separate geography, MY operator registration, connector standard/power and tariff currency.

Test code: backend: [internal/ocpi/receiver_test.go](../../chargenet-backend/internal/ocpi/receiver_test.go) TestLocationPushStoresStationAndConnectors; [internal/api/roaming_e2e_test.go](../../chargenet-backend/internal/api/roaming_e2e_test.go).

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

Supporting records: [operator-country-matrix.csv](../evidence/integration/operator-country-matrix.csv), [demo-roaming-results.json](../evidence/integration/demo-roaming-results.json).

For suite logs, search for the test name above; the following PASS line records its result.

## TC19: Status and tariff push

Procedure: Snapshot an isolated connector and tariff. Apply a valid status patch and tariff update; reload driver and portal data.

Expected: The updated availability and price reach storage and consumer APIs without changing partner ownership. Restore the fixture.

Captured result (Pass): Status/tariff receiver tests passed. A real HTTP location push changed the disposable connector to normalized INOPERATIVE in the driver API; the location was restored. A missed source tariff update was also observed through the normal scheduler.

Test code: backend: [internal/ocpi/receiver_test.go](../../chargenet-backend/internal/ocpi/receiver_test.go) TestLocationPatchUpdatesEvseStatuses and TestTariffPushRepricesConnectors.

Representative evidence: [evidence/integration/tc19-push-visibility.json](../evidence/integration/tc19-push-visibility.json)

Supporting records: [tc20-normal-scheduler.json](../evidence/integration/tc20-normal-scheduler.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC20: Pull reconciliation after a missed push

Procedure: Change an emulator location/tariff without pushing it. Let scheduled sync run; compare before/after data and timestamps. Also rerun direct sync tests.

Expected: Pull recovers the change on the next successful configured cycle. Record measured delay; an accelerated test timer is identified explicitly.

Captured result (Pass): Without any push or direct sync call, the normal 300-second scheduler recovered the disposable partner location name and tariff. The source change remained stale immediately afterwards and appeared after about 182.2 seconds. A separate 50 ms scheduler test passed with its accelerated interval labelled.

Test code: backend: [internal/ocpi/sync_test.go](../../chargenet-backend/internal/ocpi/sync_test.go); [internal/ocpi/sync.go](../../chargenet-backend/internal/ocpi/sync.go) WithSyncInterval and DefaultSyncInterval.

Additional retained code: [backend/internal/ocpi/scheduled_reconciliation_test.go](backend/internal/ocpi/scheduled_reconciliation_test.go) — TestEvidenceScheduledSyncRepairsMissedPush (accelerated scheduler).

Representative evidence: [evidence/captures/edge-tc20-after-scheduled-pull.png](../evidence/captures/edge-tc20-after-scheduled-pull.png)

Supporting records: [tc20-normal-scheduler.json](../evidence/integration/tc20-normal-scheduler.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC21: Command routing across nine combinations

Procedure: Run the existing roaming test through real loopback OCPI HTTP for every operator and MY/SG/TH combination. Correlate target URLs, party, EVSE and session.

Expected: All nine combinations use the intended operator; start, telemetry and stop refer to the same session and connector.

Captured result (Pass): All nine operator/station-country subcases passed over real loopback OCPI HTTP. Each correlated the intended operator, EVSE, live session, wallet debit and source-currency CDR, including repeated start/stop protection.

Test code: backend: [internal/api/roaming_e2e_test.go](../../chargenet-backend/internal/api/roaming_e2e_test.go) TestRoamingAcrossEveryEmulatorAndCountry; [internal/ocpi/gateway_test.go](../../chargenet-backend/internal/ocpi/gateway_test.go).

Representative evidence: [evidence/integration/operator-country-matrix.csv](../evidence/integration/operator-country-matrix.csv)

Supporting records: [backend-tests.log](../evidence/backend/backend-tests.log).

## TC22: Malformed and foreign partner data

Procedure: Submit malformed locations/tariffs, contradictory IDs and another partner identity with an otherwise valid token.

Expected: Requests receive the implemented validation/authentication error and do not alter another partner records.

Captured result (Pass): Malformed-location, malformed-tariff and foreign-partner receiver tests passed. Invalid or unowned records were rejected without changing valid stored data.

Test code: backend: [internal/ocpi/receiver_test.go](../../chargenet-backend/internal/ocpi/receiver_test.go); [internal/ocpi/sync_test.go](../../chargenet-backend/internal/ocpi/sync_test.go) TestSyncSkipsMalformedLocation.

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

For suite logs, search for the test name above; the following PASS line records its result.

## TC23: Unreachable or inactive partner

Procedure: Make one emulator unreachable, then test synchronization and command handling. Suspend a disposable partner and retry discovery/start.

Expected: The failing partner is reported; reachable partners still synchronize. Suspended inventory is hidden and unusable.

Captured result (Pass): Direct-sync tests reported the unreachable partner while processing reachable partners. Real emulator offline starts returned errors without debits or holds. The suspended disposable partner disappeared from discovery and rejected a saved-station start.

Test code: backend: [internal/ocpi/sync_test.go](../../chargenet-backend/internal/ocpi/sync_test.go) TestSyncOneReportsAnUnreachablePartner and TestSyncAllStoresEveryReachablePartner; [internal/ocpi/ocpi_test.go](../../chargenet-backend/internal/ocpi/ocpi_test.go) TestSuspendedPartnerLeavesDiscovery.

Representative evidence: [evidence/reliability/tc23-controlled-start-errors.json](../evidence/reliability/tc23-controlled-start-errors.json)

Supporting records: [backend-tests.log](../evidence/backend/backend-tests.log), [tc12-governance.json](../evidence/integration/tc12-governance.json).

## TC24: Session and CDR receivers

Procedure: Send a session update and command callback for a known session. Post a CDR twice and attempt a foreign-owner update.

Expected: Updates reach the correct session; duplicate CDR delivery preserves one settlement. Foreign-owner access is denied.

Captured result (Pass): Receiver tests passed for known-session updates, command callbacks, duplicate CDR posts and foreign-owner denial. Real competing/repeated stops preserved one CDR and debit in the runtime database.

Test code: backend: [internal/ocpi/receiver_test.go](../../chargenet-backend/internal/ocpi/receiver_test.go) TestSessionPushLinksToTheChargeNetSession, TestCommandResultReachesTheGateway and TestCDRPostSettlesTheSessionOnce.

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

Supporting records: [concurrent-stops.json](../evidence/reliability/tc28-repeated-settlement/concurrent-stops.json), [accounting-checks.json](../evidence/database/accounting-checks.json).

For suite logs, search for the test name above; the following PASS line records its result.

## TC25: Start eligibility failures

Procedure: Independently test insufficient balance, unavailable/unknown EVSE, incompatible vehicle and a second active driver session.

Expected: Each rejection reports the appropriate error with no unintended session, financial debit or remaining hold.

Captured result (Pass): The ordered start-validation and quote-acceptance failure tests passed. They exercised insufficient balance, unknown/unavailable EVSE, vehicle compatibility and a second active session; focused failed-command accounting checks found no debit or remaining hold.

Test code: backend: [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestStartValidationOrder; [internal/store/quotes_test.go](../../chargenet-backend/internal/store/quotes_test.go) TestQuoteOwnershipConsumptionAndFailure.

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

For suite logs, search for the test name above; the following PASS line records its result.

## TC26: Repeated start response

Procedure: Start with an Idempotency-Key and repeat the identical request, including a replay after a deliberately lost response. Compare IDs and database rows.

Expected: The original session is returned with replay evidence; only one session and reservation exist.

Captured result (Pass): A complete start request was sent over a real socket and zero response bytes were read. After its idempotency record committed, replay returned HTTP 201, Idempotent-Replay=true and the original session ID. The session settled once.

Test code: backend: [internal/api/roaming_e2e_test.go](../../chargenet-backend/internal/api/roaming_e2e_test.go); [internal/api/idempotency.go](../../chargenet-backend/internal/api/idempotency.go).

Representative evidence: [evidence/reliability/tc26-dropped-start-replay.json](../evidence/reliability/tc26-dropped-start-replay.json)

Supporting records: [accounting-checks.json](../evidence/database/accounting-checks.json).

## TC27: Concurrent competing starts

Procedure: Run two valid estimates concurrently for one driver; then use two different drivers competing for one connector. Release the starts together with a barrier.

Expected: Exactly one competing start wins per constraint. The losing request leaves no charge or hold.

Captured result (Pass): The existing same-driver estimate competition passed. Two separate drivers with valid estimates were then released together through a barrier: one won one session/hold; the loser retained its full balance, zero sessions and no hold or debit. This focused manager test uses a controlled transport.

Test code: backend: [internal/store/quotes_test.go](../../chargenet-backend/internal/store/quotes_test.go) TestStaleQuotesMissingRatesAndConcurrentAcceptance; [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestStartValidationOrder.

Additional retained code: [backend/internal/sessions/accounting_safety_test.go](backend/internal/sessions/accounting_safety_test.go) — TestEvidenceConcurrentDriversSameConnector.

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

For suite logs, search for the test name above; the following PASS line records its result.

## TC28: Repeated stop and concurrent settlement

Procedure: Charge positive energy, stop, repeat stop and invoke competing settlement attempts. Compare CDR and debit counts before and after.

Expected: One CDR and one positive wallet debit remain, with unchanged final amount and no remaining hold. Connector becomes available.

Captured result (Pass): Real simultaneous stop calls and a further repeated stop returned the same CDR and amount. SQL confirmed one positive debit/CDR and no held reservation. Store currency-matrix subcases also passed concurrent settlement retries.

Test code: backend: [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestStopSettlesExactlyOnce; [internal/store/quotes_test.go](../../chargenet-backend/internal/store/quotes_test.go) TestQuoteCurrencyMatrix.

Representative evidence: [evidence/database/tc28-session-cdr-wallet.csv](../evidence/database/tc28-session-cdr-wallet.csv)

Supporting records: [concurrent-stops.json](../evidence/reliability/tc28-repeated-settlement/concurrent-stops.json), [accounting-checks.json](../evidence/database/accounting-checks.json), [wallet-tariff-currency-matrix.csv](../evidence/integration/wallet-tariff-currency-matrix.csv).

## TC29: Stop timeout and uncertain completion

Procedure: Interrupt the stop callback or terminal update. Observe the timeout and mobile reconciliation; later deliver authoritative terminal state.

Expected: The interface preserves uncertainty until confirmation; no premature receipt or duplicate settlement appears. Recovery produces the correct final record.

Captured result (Pass): After hotfix ca50522, repeated unconfirmed stop responses preserve the active CHARGING session, wallet hold and live stream, with zero CDRs or debits. Later confirmed 1.000 kWh terminal telemetry creates one CDR and one MYR 1.80 debit; the wallet balance is MYR 98.20, the hold is zero and the connector is AVAILABLE. Duplicate terminal telemetry and repeated stops preserve that settlement. A separate in-flight terminal-update test returns the confirmed result. Both focused tests and the full serial backend suite pass with no test skips. Evidence uses real isolated PostgreSQL and a controlled transport.

Test code: backend: [internal/ocpi/gateway_test.go](../../chargenet-backend/internal/ocpi/gateway_test.go) TestGatewayStopSessionGivesUpWhenTheCPONeverAnswers; mobile: [test/session_coordinator_test.dart](../../chargenet-mobile/test/session_coordinator_test.dart).

Additional retained code: [backend/internal/sessions/stop_uncertainty_test.go](backend/internal/sessions/stop_uncertainty_test.go) — TestEvidenceUnknownStopPreservesUncertainty, TestEvidenceUnknownStopAfterConfirmedSettlement.

Representative evidence: [evidence/backend/stop-confirmation-tests.log](../evidence/backend/stop-confirmation-tests.log)

Supporting records: [stop-confirmation-summary.json](../evidence/backend/stop-confirmation-summary.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC30: Telemetry interruption and reconnection

Procedure: Interrupt SSE while charging, keep REST available, then interrupt all connectivity. Restore it and deliver an old frame after a newer snapshot.

Expected: Polling/reconnection restores the same session. Missing data is shown as uncertain; stale responses do not overwrite a newer session or cause a receipt.

Captured result (Pass): Complete network loss displayed interrupted updates while retaining the same session and last confirmed readings. Restoring connectivity and choosing Retry live updates resumed fresh readings without a duplicate start or settlement. The successful Android result and controlled stream-recovery tests are retained.

Test code: mobile: [test/session_stream_test.dart](../../chargenet-mobile/test/session_stream_test.dart); [test/session_coordinator_test.dart](../../chargenet-mobile/test/session_coordinator_test.dart); backend: [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestStreamCarriesTelemetryThenCompleted.

Representative evidence: [evidence/captures/android-tc30-complete-network-restored.png](../evidence/captures/android-tc30-complete-network-restored.png)

Supporting records: [android.json](../evidence/reliability/tc30-telemetry-recovery/android.json), [android-confirmed-ui-recovery.json](../evidence/reliability/tc30-telemetry-recovery/android-confirmed-ui-recovery.json), [mobile-tests.log](../evidence/mobile/mobile-tests.log).

## TC31: Recovery of an active session

Procedure: Persist positive progress, stop the manager without finalisation, create a fresh manager and gateway, and observe recovery. Separately assess a full process restart.

Expected: Persisted progress is retained, with a single final settlement and released connector/hold. State which transport and restart boundary were actually exercised.

Captured result (Pass): The active-session experiment killed and restarted the entire Go process, including its in-process emulators. Stored positive progress was retained and final accounting remained single-instance. The restarted emulator accepted the private resume extension; this does not establish persistence of an independent physical CPO.

Test code: backend: [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestRestartResumesInterruptedSession.

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

Supporting records: [before.json](../evidence/reliability/tc31-active-restart/before.json), [after.json](../evidence/reliability/tc31-active-restart/after.json), [.json](../evidence/reliability/tc31-active-restart/.json), [accounting-checks.json](../evidence/database/accounting-checks.json).

For suite logs, search for the test name above; the following PASS line records its result.

## TC32: Recovery of interrupted settlement

Procedure: Persist the settlement request, interrupt processing before final accounting, and run a new manager. Repeat recovery once more.

Expected: Accepted pricing and stopped energy remain fixed. Recovery creates one debit/CDR and releases the hold without restarting delivery.

Captured result (Pass): A durable settlement-intent fixture was persisted before abrupt process death. Recovery retained 0.778 kWh and original cost 1.17, with the accepted FX. A second restart left one debit/CDR and no hold. Existing interrupted-settlement tests passed separately.

Test code: backend: [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestRestartFinishesDurableSettlementAndReleasesHold; [internal/store/settlement_recovery.go](../../chargenet-backend/internal/store/settlement_recovery.go).

Representative evidence: [evidence/reliability/tc32-settlement-restart/recovered.json](../evidence/reliability/tc32-settlement-restart/recovered.json)

Supporting records: [tc31-tc32-after-repeated-restart.csv](../evidence/database/tc31-tc32-after-repeated-restart.csv), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC33: Pricing revalidation without expiry

Procedure: Accept an old unchanged estimate; repeat with a newer same-value FX record, a changed FX value, a changed tariff and a missing rate source.

Expected: Age alone does not reject an estimate. Changed financial terms require review; unavailable FX blocks acceptance without consuming the estimate or reserving funds.

Captured result (Pass): Current-pricing tests passed for unchanged old estimates, a newer same-value rate, changed FX/tariff and missing rates. Age alone did not invalidate the accepted quote; failed pricing review did not consume it or reserve funds.

Test code: backend: [internal/store/pricing_revalidation_test.go](../../chargenet-backend/internal/store/pricing_revalidation_test.go); [internal/store/quotes_test.go](../../chargenet-backend/internal/store/quotes_test.go) TestStaleQuotesMissingRatesAndConcurrentAcceptance.

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

Supporting records: [backend-test-summary.json](../evidence/backend/backend-test-summary.json).

For suite logs, search for the test name above; the following PASS line records its result.

## TC34: Currency matrix and locked settlement

Procedure: Run all nine wallet/tariff currency pairs. Change tariff/FX after acceptance, settle and compare original charge, wallet debit and retained receipt.

Expected: Settlement uses accepted values. The wallet and CDR retain their own currencies; subsequent updates do not rewrite the historical receipt.

Captured result (Pass): All nine wallet/tariff currency subcases and locked historical-rate tests passed. Runtime SGD and THB journeys retained original charges and accepted conversion in MYR receipts and matching CDR/debit rows. These nine currency pairs are distinct from the nine operator/country cases.

Test code: backend: [internal/store/quotes_test.go](../../chargenet-backend/internal/store/quotes_test.go) TestQuoteCurrencyMatrix and TestLockedRateAndHistoricalReceipt; mobile: [test/multi_currency_test.dart](../../chargenet-mobile/test/multi_currency_test.dart).

Representative evidence: [evidence/integration/wallet-tariff-currency-matrix.csv](../evidence/integration/wallet-tariff-currency-matrix.csv)

Supporting records: [tc09-mobile-chargesync-journey.json](../evidence/integration/tc09-mobile-chargesync-journey.json), [tc09-mobile-ecowatt-journey.json](../evidence/integration/tc09-mobile-ecowatt-journey.json), [accounting-checks.json](../evidence/database/accounting-checks.json).

## TC35: Automatic stop and zero cost boundary

Procedure: Run target reached and balance exhausted cases; stop a zero-energy session. Inspect wallet liability fields and repeat settlement.

Expected: Automatic stops preserve valid terminal state. Debit never exceeds available funds; any unfunded amount is traceable. Zero energy creates no positive debit or duplicate record.

Captured result (Pass): Existing target-reached and wallet-exhaustion guards passed. A focused real local-simulator test stopped before any timer tick: three stops left zero energy/cost, one zero-value CDR, zero debits, unchanged balance, released hold and available connector.

Test code: backend: [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestStartChargingSettlesAtTarget and TestWalletExhaustedStopsAndClampsSettlement; [internal/store/sessions.go](../../chargenet-backend/internal/store/sessions.go).

Additional retained code: [backend/internal/sessions/accounting_safety_test.go](backend/internal/sessions/accounting_safety_test.go) — TestEvidenceZeroEnergyRepeatedStop.

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

For suite logs, search for the test name above; the following PASS line records its result.

## TC36: Driver ownership boundaries

Procedure: As a second driver, request another driver vehicle, estimate, session, stream and history identifiers through direct API calls.

Expected: No private record or financial action is exposed. Record exact denial status and verify unchanged stored data.

Captured result (Pass): Vehicle/quote ownership and subscription tests passed. Direct HTTP calls by another driver to the completed session and stream returned denial. The second account received no private session data.

Test code: backend: [internal/api/vehicle_handler_test.go](../../chargenet-backend/internal/api/vehicle_handler_test.go) TestVehicleOwnershipIsolation; [internal/store/quotes_test.go](../../chargenet-backend/internal/store/quotes_test.go) TestQuoteOwnershipConsumptionAndFailure; [internal/sessions/manager_test.go](../../chargenet-backend/internal/sessions/manager_test.go) TestSubscribeHidesAnotherDriversSession.

Representative evidence: [evidence/requests/tc36-tc37-tc38-access-denials.json](../evidence/requests/tc36-tc37-tc38-access-denials.json)

Supporting records: [backend-tests.log](../evidence/backend/backend-tests.log).

## TC37: Portal role and tenant boundaries

Procedure: Use no cookie, a CPO cookie and a different CPO identity against protected endpoints, CDR details and administrator actions.

Expected: Unauthenticated and unauthorised requests fail. One operator cannot read another operator financial records or approve partners.

Captured result (Pass): Unauthenticated portal access returned 401; a CPO administrator request returned 403; a foreign CPO CDR request returned 404. Existing tenancy/export tests also passed.

Test code: backend: [internal/api/portal_test.go](../../chargenet-backend/internal/api/portal_test.go) TestPortalRequiresSession, TestPortalAdminConsoleAndTenancy and TestPortalCDRDetailIsTenancyScopedAndFilterableByEVSE.

Representative evidence: [evidence/requests/tc36-tc37-tc38-access-denials.json](../evidence/requests/tc36-tc37-tc38-access-denials.json)

Supporting records: [backend-tests.log](../evidence/backend/backend-tests.log).

## TC38: OCPI token contract

Procedure: Use missing/unknown tokens, used Token A and a valid token naming a different party against module and callback endpoints.

Expected: Only the allowed token/party/module combination succeeds; rejected requests leave records unchanged.

Captured result (Pass): Missing and unknown operational tokens were rejected through direct HTTP. Existing token-contract, wrong-party/module and foreign callback/receiver tests passed; consumed and rotated credentials were denied in the live disposable-partner experiment.

Test code: backend: [internal/ocpi/ocpi_test.go](../../chargenet-backend/internal/ocpi/ocpi_test.go) TestModuleEndpointsEnforceTheTokenContract and TestMissingOrUnknownTokenIsRejected; [internal/ocpi/receiver_test.go](../../chargenet-backend/internal/ocpi/receiver_test.go).

Representative evidence: [evidence/requests/tc36-tc37-tc38-access-denials.json](../evidence/requests/tc36-tc37-tc38-access-denials.json)

Supporting records: [tc17-tc13-token-lifecycle.json](../evidence/integration/tc17-tc13-token-lifecycle.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC39: Login throttling and session expiry

Procedure: Repeat incorrect portal login until the configured threshold is reached, then test an expired session and logout in the browser.

Expected: Configured login throttling returns the expected rate-limit response. Expired/logout state removes protected access and stale account views.

Captured result (Pass): The configured five-failure login throttle test passed. A correctly signed expired portal JWT removed protected browser access; invalid-session and logout navigation checks also passed and cleared sandbox state.

Test code: backend: [internal/api/portal_test.go](../../chargenet-backend/internal/api/portal_test.go) TestPortalLoginRateLimited; portal: [src/api.ts](../../chargenet-portal/src/api.ts); [src/auth/AuthContext.tsx](../../chargenet-portal/src/auth/AuthContext.tsx).

Representative evidence: [evidence/portal/browser-checks.json](../evidence/portal/browser-checks.json)

Supporting records: [browser-workflow-results.json](../evidence/portal/browser-workflow-results.json), [backend-tests.log](../evidence/backend/backend-tests.log).

## TC40: Small-screen and scalable text

Procedure: Run existing 320 by 640 and 640 by 320 widget layouts at 100% and 200% text. Inspect estimate, profile, discovery and charging controls on Android.

Expected: Required actions remain reachable without overflow or clipped financial figures. Record each viewport and scale.

Captured result (Pass): Flutter layout tests passed at 320x640 and 640x320 with 100%/200% text. Android 320dp/200% profile and estimate views were captured, and scrolling exposed required profile and confirmation controls. The original size and text scale were restored.

Test code: mobile: [test/layout_test.dart](../../chargenet-mobile/test/layout_test.dart); [test/typesetting_test.dart](../../chargenet-mobile/test/typesetting_test.dart); [test/multi_currency_test.dart](../../chargenet-mobile/test/multi_currency_test.dart).

Representative evidence: [evidence/captures/android-tc40-320dp-200-confirmation-full-label.png](../evidence/captures/android-tc40-320dp-200-confirmation-full-label.png)

Supporting records: [mobile-tests.log](../evidence/mobile/mobile-tests.log), [tc40-android-controls.json](../evidence/mobile/tc40-android-controls.json).

## TC41: Accessible confirmation and light appearance

Procedure: Test keyboard/focus or assistive confirmation alternatives, interrupted dragging, busy controls and onboarding semantics; inspect representative screens in light mode.

Expected: Confirmation is accessible, cancelled drags submit nothing, duplicate busy actions are prevented and visible screens retain the light theme.

Captured result (Pass): Accessible start and stop confirmation alternatives were used on Android. Widget tests passed cancelled drags, busy controls and onboarding semantics; sampled Android and portal screens retained the light appearance. This is not accessibility certification.

Test code: mobile: [test/interaction_accessibility_test.dart](../../chargenet-mobile/test/interaction_accessibility_test.dart); [test/slide_to_confirm_test.dart](../../chargenet-mobile/test/slide_to_confirm_test.dart); [lib/core/app_theme.dart](../../chargenet-mobile/lib/core/app_theme.dart); portal: [src/app.css](../../chargenet-portal/src/app.css).

Representative evidence: [evidence/mobile/mobile-tests.log](../evidence/mobile/mobile-tests.log)

Supporting records: [tc40-android-controls.json](../evidence/mobile/tc40-android-controls.json).

For suite logs, search for the test name above; the following PASS line records its result.

## TC42: Portal layout and browser compatibility

Procedure: Use available Chromium and Firefox at desktop and narrow widths. Check login, overview, ledger, network and admin navigation by keyboard.

Expected: Data, navigation, errors and financial controls remain readable and operable at each recorded viewport. Unsupported browser availability is recorded as blocked.

Captured result (Pass): Edge and Firefox passed eight sampled CPO route/width checks each, with keyboard focus and no document overflow. Edge administrator navigation also passed at desktop and narrow widths. Financial tables retain their own horizontal scroll region where needed.

Test code: portal: [src/App.tsx](../../chargenet-portal/src/App.tsx); [src/layout/Shell.tsx](../../chargenet-portal/src/layout/Shell.tsx); [src/pages/](../../chargenet-portal/src/pages/); [src/app.css](../../chargenet-portal/src/app.css).

Representative evidence: [evidence/captures/edge-tc42-390-ledger.png](../evidence/captures/edge-tc42-390-ledger.png)

Supporting records: [layout-browser-matrix.csv](../evidence/performance/layout-browser-matrix.csv), [firefox-results.json](../evidence/portal/firefox-results.json), [browser-checks.json](../evidence/portal/browser-checks.json).

## TC43: Measured local response and update delay

Procedure: Under a stated local fixture size, collect 30 timed station reads after five warm-ups; separately timestamp start-to-first-telemetry, pushed updates and scheduled reconciliation.

Expected: Report sample count, median, p95, errors and conditions. Treat timing as descriptive unless a justified threshold is agreed before execution.

Captured result (Pass): Descriptive measurement completed: five warm-ups and 30 station reads at the recorded 38-station fixture, plus start-to-first positive SSE, push visibility and normal scheduled-pull delay. No numerical SLA or production-capacity conclusion is applied.

Test code: backend: /api/v1/stations; /api/v1/sessions/{id}/stream; [internal/ocpi/sync.go](../../chargenet-backend/internal/ocpi/sync.go).

Representative evidence: [evidence/performance/timing-summary.json](../evidence/performance/timing-summary.json)

Supporting records: [timing-samples.csv](../evidence/performance/timing-samples.csv), [tc43-start-to-first-sse.json](../evidence/performance/tc43-start-to-first-sse.json), [tc19-push-visibility.json](../evidence/integration/tc19-push-visibility.json), [tc20-normal-scheduler.json](../evidence/integration/tc20-normal-scheduler.json).

## TC44: Persistent migration and seed safety

Procedure: Use a disposable legacy fixture containing completed sessions and ledger records. Apply ordered migrations twice, then compare stored values and inventory IDs.

Expected: Historical financial values and custom names survive; seeds/migrations do not duplicate the regional inventory.

Captured result (Pass): The disposable legacy migration/history-preservation and inventory seed-idempotency tests passed. This verifies their stored financial/custom-name/inventory assertions within the existing fixtures.

Test code: backend: [internal/store/migration_test.go](../../chargenet-backend/internal/store/migration_test.go) TestUpgradePreservesLegacyFinancialHistory; [internal/store/quotes_test.go](../../chargenet-backend/internal/store/quotes_test.go) TestStationGeographyAndSeedIdempotency; [scripts/migrations/](../../chargenet-backend/scripts/migrations/).

Representative evidence: [evidence/backend/backend-tests.log](../evidence/backend/backend-tests.log)

Supporting records: [backend-test-summary.json](../evidence/backend/backend-test-summary.json).

For suite logs, search for the test name above; the following PASS line records its result.
