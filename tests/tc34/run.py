from capture import *
for currency in ['MYR','SGD','THB']:
 c=Client(currency);user=c.register();sql("UPDATE wallets SET currency='"+currency+"' WHERE user_id='"+user['user']['id']+"';");c.fund(500)
 for country in ['MY','SG','TH']:
  note('MATRIX wallet='+currency+'; tariff country='+country);station,k=c.pick(country);q=c.quote(k);s=c.start(k,q)
  original=sql("SELECT id,price_per_kwh,last_updated FROM tariffs WHERE id='"+q['tariffId']+"';")[0]
  try:
   sql("UPDATE tariffs SET price_per_kwh=price_per_kwh+0.10,last_updated=clock_timestamp() WHERE id='"+q['tariffId']+"';")
   if currency!=q['originalCurrency']:
    sql("INSERT INTO exchange_rates(id,source_currency,target_currency,rate,effective_at,source) VALUES ('fx_"+uuid.uuid4().hex+"','"+q['originalCurrency']+"','"+currency+"',"+str(float(q['exchangeRate'])*1.1)+",clock_timestamp(),'chapter-five-matrix');")
   c.positive(s);c.call('POST','/api/v1/sessions/'+s['id']+'/stop');accounting(s['id']);c.call('GET','/api/v1/wallet/transactions');c.call('GET','/api/v1/sessions/'+s['id'])
  finally:
   sql("UPDATE tariffs SET price_per_kwh="+original['price_per_kwh']+",last_updated='"+original['last_updated']+"' WHERE id='"+q['tariffId']+"';")
   if currency!=q['originalCurrency']:sql("INSERT INTO exchange_rates(id,source_currency,target_currency,rate,effective_at,source) VALUES ('fx_"+uuid.uuid4().hex+"','"+q['originalCurrency']+"','"+currency+"',"+q['exchangeRate']+",clock_timestamp(),'chapter-five-restore');")
  c.call('GET','/api/v1/sessions/'+s['id'])
