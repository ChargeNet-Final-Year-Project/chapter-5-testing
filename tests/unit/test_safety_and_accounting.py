import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tests'))
from accounting_assertions import accounting_checks
from run_checks import go_summary
from test_support import clean, validate_runtime_dsn, validate_test_dsn


class DatabaseIsolation(unittest.TestCase):
    def test_disposable_test_database_is_accepted(self):
        self.assertEqual(validate_test_dsn('postgresql://local:unused@localhost:55433/chargenet_test'), 'chargenet_test')

    def test_application_and_runtime_databases_are_rejected_for_sql_tests(self):
        for name in ['chargenet', 'production', 'chargenet_evidence_test', 'other_test', '']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate_test_dsn('postgresql://local:unused@localhost/' + name)

    def test_runtime_cannot_use_the_destructive_test_database(self):
        with self.assertRaises(ValueError):
            validate_runtime_dsn('postgresql://local:unused@localhost/chargenet_test')

    def test_credentials_are_removed_from_command_output(self):
        with patch.dict(os.environ, {'CHARGENET_DRIVER_PASSWORD': 'disposable-secret'}):
            output = clean('postgresql://local:unused@localhost/chargenet_test disposable-secret')
        self.assertNotIn('local:unused', output)
        self.assertNotIn('disposable-secret', output)


class TestEventAccounting(unittest.TestCase):
    def test_packages_without_tests_are_not_counted_as_skipped_assertions(self):
        events = [dict(Action='skip', Package='empty'), dict(Action='pass', Package='sessions', Test='TestStop'), dict(Action='skip', Package='sessions', Test='TestSQL')]
        summary = go_summary('\n'.join(json.dumps(event) for event in events))
        self.assertEqual(summary['test_events'], {'pass': 1, 'fail': 0, 'skip': 1})

    def test_package_failure_is_preserved_without_a_failed_test_event(self):
        summary = go_summary(json.dumps(dict(Action='fail', Package='cannot-build')))
        self.assertEqual(summary['failed_packages'], ['cannot-build'])


class SettlementChecks(unittest.TestCase):
    def setUp(self):
        self.row = dict(session_id='synthetic-session', kwh_delivered='1.000', total_cost='1.80', cdr_count='1', debit_count='1', debit_amount='1.80', reserved='0', connector_status='AVAILABLE', cdr_currency='MYR', original_currency='MYR', gross_amount='1.80', original_cost='1.80', platform_fee='0.09', net_payout='1.71', exchange_rate='1.0')

    def test_consistent_settlement_passes(self):
        self.assertEqual(accounting_checks([self.row])[0]['status'], 'Pass')

    def test_duplicate_debit_is_rejected(self):
        self.row['debit_count'] = '2'
        self.assertEqual(accounting_checks([self.row])[0]['status'], 'Fail')

    def test_unreleased_reservation_is_rejected(self):
        self.row['reserved'] = '1.80'
        self.assertEqual(accounting_checks([self.row])[0]['status'], 'Fail')

    def test_zero_energy_and_zero_cost_need_no_debit(self):
        self.row.update(kwh_delivered='0', total_cost='0', debit_amount='0', debit_count='0')
        self.assertEqual(accounting_checks([self.row])[0]['status'], 'Pass')


if __name__ == '__main__':
    unittest.main()
