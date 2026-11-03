from decimal import Decimal, ROUND_HALF_UP


def accounting_checks(rows):
    checks = []
    for row in rows:
        positive = Decimal(row['kwh_delivered']) > 0 and Decimal(row['total_cost']) > 0
        conditions = dict(one_cdr=int(row['cdr_count']) == 1 if positive else True, one_debit=int(row['debit_count']) == 1 if positive else int(row['debit_count']) == 0, debit_equals_cost=Decimal(row['debit_amount']) == Decimal(row['total_cost']), hold_released=Decimal(row['reserved']) == 0, connector_available=row['connector_status'] == 'AVAILABLE')
        if positive:
            conditions.update(cdr_currency_preserved=row['cdr_currency'] == row['original_currency'], cdr_gross_matches=Decimal(row['gross_amount']) == Decimal(row['original_cost']), fee_plus_net_equals_gross=Decimal(row['platform_fee']) + Decimal(row['net_payout']) == Decimal(row['gross_amount']), locked_fx_wallet_rounding=(Decimal(row['original_cost']) * Decimal(row['exchange_rate'])).quantize(Decimal('.01'), ROUND_HALF_UP) == Decimal(row['total_cost']))
        checks.append(dict(session_id=row['session_id'], positive_energy_cost=positive, conditions=conditions, status='Pass' if all(conditions.values()) else 'Fail'))
    return checks
