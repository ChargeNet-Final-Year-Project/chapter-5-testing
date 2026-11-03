# ChargeNet Chapter 5 Testing

TC01-TC44 are complete and passed for the documented test scope. Each [test folder](tests) contains its procedure, expected result, observed result and supporting evidence.

Coverage includes backend and mobile regression, portal builds, driver journeys, partner integration, charging recovery, financial reconciliation, security, accessibility and migration safety.

Recorded results include:

- 133 backend tests passed; Go vet and build succeeded.
- 265 Flutter tests passed; analysis and the Android debug build succeeded.
- Portal TypeScript checks and the production build succeeded.
- Revenue exports reconciled across MYR, SGD and THB.

See [setup instructions](SETUP.md) for tool versions, application revisions and local services. From a case folder, run `python run.py` or the commands listed in its README. Run cases that use the services sequentially against the isolated test databases.
