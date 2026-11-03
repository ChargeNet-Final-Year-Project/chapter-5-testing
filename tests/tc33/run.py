from capture import *
def rate(value):sql("INSERT INTO exchange_rates(id,source_currency,target_currency,rate,effective_at,source) VALUES ('fx_"+uuid.uuid4().hex+"','SGD','MYR',"+str(value)+",clock_timestamp(),'chapter-five-disposable');")
for scenario in ['old-unchanged','new-record-same-rate','changed-rate','changed-tariff','missing-source']:
 note('SCENARIO '+scenario);c=Client(scenario);user=c.register();c.fund(500);station,k=c.pick('SG','cpo_chargesync');rate('3.45');q=c.quote(k)
 original=sql("SELECT id,price_per_kwh,last_updated FROM tariffs WHERE id='"+q['tariffId']+"';")[0]
 try:
  if scenario in ['old-unchanged','missing-source']:
   clone='qte_'+uuid.uuid4().hex;source="rate_selection_source" if scenario=='old-unchanged' else "'missing-disposable-source'"
   sql("INSERT INTO charging_quotes (id,user_id,wallet_id,cpo_id,station_id,connector_id,tariff_id,tariff_updated_at,tariff_per_kwh,original_currency,wallet_currency,exchange_rate_id,exchange_rate,rate_source,estimated_kwh,estimated_original_cost,estimated_wallet_cost,budget,created_at,expires_at,rate_selection_source) SELECT '"+clone+"',user_id,wallet_id,cpo_id,station_id,connector_id,tariff_id,tariff_updated_at,tariff_per_kwh,original_currency,wallet_currency,exchange_rate_id,exchange_rate,rate_source,estimated_kwh,estimated_original_cost,estimated_wallet_cost,budget,now()-interval '1 year',now()-interval '364 days',"+source+" FROM charging_quotes WHERE id='"+q['id']+"';")
   q['id']=clone
  if scenario=='new-record-same-rate':rate('3.4500000000')
  if scenario=='changed-rate':rate('3.55')
  if scenario=='changed-tariff':sql("UPDATE tariffs SET price_per_kwh=price_per_kwh+0.01,last_updated=clock_timestamp() WHERE id='"+q['tariffId']+"';")
  s=c.start(k,q);c.call('GET','/api/v1/wallet');sql("SELECT id,accepted_at,exchange_rate,rate_source,rate_selection_source FROM charging_quotes WHERE id='"+q['id']+"';")
  if s.get('id'):c.positive(s);c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id'])
 finally:
  rate('3.45');sql("UPDATE tariffs SET price_per_kwh="+original['price_per_kwh']+",last_updated='"+original['last_updated']+"' WHERE id='"+q['tariffId']+"';")
