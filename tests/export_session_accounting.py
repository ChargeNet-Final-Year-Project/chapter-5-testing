from accounting_assertions import accounting_checks
from test_api_and_accounting import sql, save, ACCOUNTING


def export():
    checks = accounting_checks(sql(ACCOUNTING, 'evidence/database/session-cdr-wallet.csv'))
    save('evidence/database/accounting-checks.json', checks)
    assert checks and all(row['status'] == 'Pass' for row in checks), checks
    print('Accounting invariants checked:', len(checks), 'sessions')


if __name__ == '__main__':
    export()
