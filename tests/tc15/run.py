from capture import *
from ui import *
from urllib.parse import urlencode
fixture = "INSERT INTO users(id,name,email,password_hash) VALUES ('usr_report_evidence','Chapter Five reporting fixture','report-evidence@example.test','not-a-login') ON CONFLICT DO NOTHING;\n"
for currency, country in [('MYR', 'MY'), ('SGD', 'SG'), ('THB', 'TH')]:
    station = sql("SELECT s.id AS station,k.id AS connector,k.evse_uid FROM stations s JOIN connectors k ON k.station_id=s.id WHERE s.cpo_id='cpo_voltgo' AND s.country_code='" + country + "' AND k.power_type='DC' ORDER BY s.id LIMIT 1;")[0]
    for label, n, at, user in [('inside', 26, '2026-10-31T16:00:00Z', 'usr_report_evidence'), ('before', 1, '2026-10-31T15:59:59.999999Z', 'usr_report_evidence'), ('after', 1, '2026-11-01T16:00:00Z', 'usr_report_evidence'), ('sandbox', 1, '2026-10-31T17:00:00Z', 'usr_sandbox')]:
        prefix = 'report_' + currency + '_' + label + '_'
        fixture += f"INSERT INTO charging_sessions(id,user_id,cpo_id,station_id,connector_id,evse_uid,status,start_time,end_time,duration_seconds,kwh_delivered,tariff_per_kwh,total_cost,original_currency,wallet_currency,exchange_rate,original_cost)\nSELECT '{prefix}'||i,'{user}','cpo_voltgo','{station['station']}','{station['connector']}','{station['evse_uid']}','COMPLETED','{at}'::timestamptz-interval '1 minute','{at}'::timestamptz,60,1,1.60,1.60,'{currency}','{currency}',1,1.60 FROM generate_series(1,{n}) i ON CONFLICT DO NOTHING;\nINSERT INTO cdrs(id,session_id,cpo_id,user_id,total_energy_kwh,total_time_seconds,gross_amount,platform_fee,net_payout,currency,cdr_json,created_at)\nSELECT 'cdr_{prefix}'||i,'{prefix}'||i,'cpo_voltgo','{user}',1,60,1.60,0.08,1.52,'{currency}','{{}}','{at}'::timestamptz FROM generate_series(1,{n}) i ON CONFLICT DO NOTHING;\n"
sql(fixture)
c=Client('operator');c.call('POST','/admin/api/login',dict(email='ops@voltgo.my',password='Cpo1234!'))
for currency in ['MYR','SGD','THB']:
 query=urlencode(dict(currency=currency,**{'from':'2026-11-01','to':'2026-11-01'}))
 c.call('GET','/admin/api/overview?currency='+currency);c.call('GET','/admin/api/cdrs?'+query);c.call('GET','/admin/api/cdrs?'+query+'&page=2')
 csv=c.call('GET','/admin/api/cdrs?'+query+'&format=csv&limit=1&page=99');(HERE/(currency+'-full-export.csv')).write_text(csv,encoding='utf-8')
 sql("SELECT currency,count(*) AS cdrs,sum(gross_amount) AS gross,sum(platform_fee) AS fee,sum(net_payout) AS net FROM cdrs WHERE cpo_id='cpo_voltgo' AND user_id<>'usr_sandbox' AND currency='"+currency+"' AND created_at>='2026-10-31T16:00:00Z' AND created_at<'2026-11-01T16:00:00Z' GROUP BY currency;")
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);page=b.new_page(viewport={'width':1440,'height':1000},timezone_id='Asia/Kuala_Lumpur');login(page)
 page.goto('http://localhost:15173/#/ledger');page.wait_for_timeout(800)
 for currency in ['MYR','SGD','THB']:
  page.get_by_label('From',exact=True).fill('2026-11-01');page.get_by_label('To',exact=True).fill('2026-11-01');page.get_by_label('Revenue currency',exact=True).select_option(currency);page.wait_for_timeout(700);shot(page,currency+'-ledger')
  with page.expect_download() as d:page.get_by_role('button',name='Export CSV',exact=True).click()
  d.value.save_as(str(HERE/(currency+'-browser-export.csv')))
 page.goto('http://localhost:15173/#/overview');page.wait_for_timeout(800)
 for currency in ['MYR','SGD','THB']:
  page.get_by_label('Revenue currency',exact=True).select_option(currency);page.wait_for_timeout(700);shot(page,currency+'-overview')
 sql("SELECT currency,count(*) AS count,sum(gross_amount) AS gross,sum(net_payout) AS net FROM cdrs WHERE cpo_id='cpo_voltgo' AND user_id<>'usr_sandbox' AND created_at>='2026-10-31T16:00:00Z' AND created_at<'2026-11-30T16:00:00Z' GROUP BY currency ORDER BY currency;")
 b.close()
