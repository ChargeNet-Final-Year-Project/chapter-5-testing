import os
import csv
import io
from decimal import Decimal
from urllib.parse import urlencode
from test_support import RUN,now
from test_api_and_accounting import Client,sql,save

def run():
    # Synthetic report fixtures are direct SQL inserts, not simulated charging
    # journeys. Their identifiers start report_ and they create no wallet debit.
    fixture="""INSERT INTO users(id,name,email,password_hash) VALUES ('usr_report_evidence','Synthetic reporting fixture','report-evidence@example.test','not-a-login') ON CONFLICT DO NOTHING;
"""
    for currency,country in [('MYR','MY'),('SGD','SG'),('THB','TH')]:
        station=sql("SELECT s.id AS station,k.id AS connector,k.evse_uid FROM stations s JOIN connectors k ON k.station_id=s.id WHERE s.cpo_id='cpo_voltgo' AND s.country_code='"+country+"' AND k.power_type='DC' ORDER BY s.id LIMIT 1;")[0]
        for label,n,at,user in [('inside',26,'2026-10-25T16:00:00Z','usr_report_evidence'),('before',1,'2026-10-25T15:59:59.999999Z','usr_report_evidence'),('after',1,'2026-10-26T16:00:00Z','usr_report_evidence'),('sandbox',1,'2026-10-25T17:00:00Z','usr_sandbox')]:
            prefix='report_'+currency+'_'+label+'_'
            fixture+=f"""INSERT INTO charging_sessions(id,user_id,cpo_id,station_id,connector_id,evse_uid,status,start_time,end_time,duration_seconds,kwh_delivered,tariff_per_kwh,total_cost,original_currency,wallet_currency,exchange_rate,original_cost)
SELECT '{prefix}'||i,'{user}','cpo_voltgo','{station['station']}','{station['connector']}','{station['evse_uid']}','COMPLETED','{at}'::timestamptz-interval '1 minute','{at}'::timestamptz,60,1,1.60,1.60,'{currency}','{currency}',1,1.60 FROM generate_series(1,{n}) i ON CONFLICT DO NOTHING;
INSERT INTO cdrs(id,session_id,cpo_id,user_id,total_energy_kwh,total_time_seconds,gross_amount,platform_fee,net_payout,currency,cdr_json,created_at)
SELECT 'cdr_{prefix}'||i,'{prefix}'||i,'cpo_voltgo','{user}',1,60,1.60,0.08,1.52,'{currency}','{{}}','{at}'::timestamptz FROM generate_series(1,{n}) i ON CONFLICT DO NOTHING;
"""
    sql(fixture,'evidence/database/tc15-synthetic-reporting-fixture.csv')
    c=Client();assert c.call('POST','/admin/api/login',dict(email='ops@voltgo.my',password=os.environ.get('CHARGENET_OPERATOR_PASSWORD', '')))[0]==200
    outcomes=[]
    for currency in ['MYR','SGD','THB']:
        query=urlencode(dict(currency=currency,**{'from':'2026-10-26','to':'2026-10-26'}));base='/admin/api/cdrs?'+query
        status,first,_=c.call('GET',base);assert status==200
        status,second,_=c.call('GET',base+'&page=2');assert status==200
        status,raw,_=c.call('GET',base+'&format=csv&limit=1&page=99');assert status==200
        dest=RUN/f'evidence/integration/TC15_full_range_{currency}.csv';dest.write_text(raw,encoding='utf8')
        rows=list(csv.reader(io.StringIO(raw)));data=rows[1:-1]
        assert len(first['rows'])==25 and len(second['rows'])==1 and len(data)==26
        assert all('report_'+currency+'_inside_' in x[0] for x in data)
        assert Decimal(rows[-1][9])==Decimal('41.60') and Decimal(rows[-1][11])==Decimal('39.52'),rows[-1]
        db=sql("SELECT currency,count(*) AS cdrs,sum(gross_amount) AS gross,sum(platform_fee) AS fee,sum(net_payout) AS net FROM cdrs WHERE cpo_id='cpo_voltgo' AND user_id<>'usr_sandbox' AND currency='"+currency+"' AND created_at>='2026-10-25T16:00:00Z' AND created_at<'2026-10-26T16:00:00Z' GROUP BY currency;",f'evidence/database/TC15_totals_{currency}.csv')
        assert int(db[0]['cdrs'])==26 and Decimal(db[0]['gross'])==Decimal('41.60')
        outcomes.append(dict(currency=currency,timezone='Asia/Kuala_Lumpur',from_date='2026-10-26',to_date='2026-10-26',json_page_1=len(first['rows']),json_page_2=len(second['rows']),csv_records=len(data),gross=rows[-1][9],net=rows[-1][11],database=db,status='Pass',fixture_type='direct SQL reporting records; no charging or wallet debit'))
    save('evidence/integration/tc15-currency-midnight-pagination.json',outcomes)
    print(outcomes)

if __name__=='__main__':run()
