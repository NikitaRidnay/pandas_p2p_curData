import pandas as pd
import requests
from pprint import pprint
import json

def get_p2p_page_sell(url, page, rows):
    headers = {'content-type': 'application/json'}
    json_data = {
        "page":page,
        "rows":rows,
        "asset":"USDT",
        "fiat":"RUB",
        "payTypes": ["TinkoffNew","RosBankNew","RaiffeisenBank"],
        "tradeType":"SELL"
    }
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code != 200:
        response.raise_for_status()
    return json.loads(response.text)

url = r'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
pprint(get_p2p_page_sell(url,1,1), depth=3)

rows = []
page = 0
while True:
    page += 1
    r = get_p2p_page_sell(url, page, 20)
    if r['data'] == []:
        break
    for i in r['data']:
        limit = float(i['adv']['minSingleTransAmount'])
        max_limit = float(i['adv']['dynamicMaxSingleTransAmount'])
        
        if limit != 100000.0 or max_limit != 500000.0:
            continue
        rows.append([
            i['advertiser']['nickName'],
            i['advertiser']['monthOrderCount'],
            i['advertiser']['monthFinishRate'],
            i['adv']['price'],
            i['adv']['fiatUnit'],
            i['adv']['commissionRate'],
            i['adv']['tradableQuantity'],
            i['adv']['asset'],
            i['adv']['minSingleTransAmount'],
            i['adv']['minSingleTransQuantity'],
            i['adv']['dynamicMaxSingleTransAmount'],
            i['adv']['dynamicMaxSingleTransQuantity'],
            i['adv']['tradeMethods'][0]['tradeMethodName'],
            i['advertiser']['userNo']])

if len(rows) == 0:
    print("No results")
else:
    df = pd.DataFrame(rows)
    columns = [
        ['Advertisers (completion rate)']*3 + ['Price']*3 + ['Available']*2 + ['Limit Amount & Quantity']*4 + ['']*2,
        ['Name', 'Orders', 'Completion', 'Price', 'Fiat', 'Comission', 'Available', 'Asset'
         , 'minA', 'minQ','maxA','maxQ','Payment','advertiserNo'],
    ]
    df.columns = pd.MultiIndex.from_tuples(list(zip(*columns)))
    print(df)
    df.to_csv('binanceP2Psell.csv')
    print('https://p2p.binance.com/en/advertiserDetail?advertiserNo=' + df.iloc[0,-1])


       
