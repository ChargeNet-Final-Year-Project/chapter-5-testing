SELECT s.id AS session_id,s.user_id,s.status,s.kwh_delivered,s.original_currency,s.original_cost,s.wallet_currency,s.exchange_rate,s.total_cost,(SELECT q.budget FROM charging_quotes q WHERE q.id=s.quote_id) AS accepted_budget,s.unfunded_amount,s.cdr_id,
 (SELECT count(*) FROM cdrs c WHERE c.session_id=s.id) AS cdr_count,
 (SELECT count(*) FROM wallet_transactions t WHERE t.session_id=s.id AND t.type='CHARGING_DEBIT') AS debit_count,
 (SELECT coalesce(sum(t.amount),0) FROM wallet_transactions t WHERE t.session_id=s.id AND t.type='CHARGING_DEBIT') AS debit_amount,
 w.balance,(SELECT coalesce(sum(r.amount),0) FROM wallet_reservations r WHERE r.wallet_id=w.id AND r.status='HELD') AS reserved,k.status AS connector_status,c.currency AS cdr_currency,c.gross_amount,c.platform_fee,c.net_payout
 FROM charging_sessions s JOIN wallets w ON w.user_id=s.user_id JOIN connectors k ON k.id=s.connector_id LEFT JOIN cdrs c ON c.session_id=s.id
 WHERE s.id NOT LIKE 'report_%' ORDER BY s.start_time;