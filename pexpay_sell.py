import pandas as pd
import requests
from pprint import pprint
import json

def get_p2p_page(url, page, rows):
    headers = {'content-type': 'application/json'}
    json_data = {
        "page":page,
        "rows":rows,
        "asset":"USDT",
        "fiat":"RUB",
        "payTypes": ["Tinkoff","RaiffeisenBankRussia","Sberbank"],
        "tradeType":"SELL"
    }
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code != 200:
        response.raise_for_status()
    return json.loads(response.text)

url = r'https://www.pexpay.com/bapi/c2c/v1/friendly/c2c/ad/search'
pprint(get_p2p_page(url,1,1), depth=3)

rows = []
page = 0
while True:
    page += 1
    r = get_p2p_page(url, page, 20)
    if r['data'] == []:
        break
    for i in r['data']:
        limit = float(i['adDetailResp']['minSingleTransAmount'])
        max_limit = float(i['adDetailResp']['dynamicMaxSingleTransAmount'])
        
        if limit != 10000.0 or max_limit != 100000.0:
            continue
        rows.append([
            i['advertiserVo']['nickName'],
            i['advertiserVo']['userStatsRet']['completedOrderNum'],
            i['advertiserVo']['userStatsRet']['completedOrderNumOfLatest30day'],
            i['adDetailResp']['price'],
            i['adDetailResp']['fiatCurrency'],
            i['adDetailResp']['commissionRate'],
            i['adDetailResp']['tradableQuantity'],
            i['adDetailResp']['asset'],
            i['adDetailResp']['minSingleTransAmount'],
            i['adDetailResp']['minSingleTransQuantity'],
            i['adDetailResp']['dynamicMaxSingleTransAmount'],
            i['adDetailResp']['maxSingleTransQuantity'],
            i['adDetailResp']['tradeMethods'][0]['tradeMethodName'],])

if len(rows) == 0:
    print("No results")
else:
    df = pd.DataFrame(rows)
    columns = [
        ['Advertisers (completion rate)']*3 + ['Price']*3 + ['Available']*2 + ['Limit Amount & Quantity']*4 + ['']*2,
        ['Name', 'Orders', 'Completion', 'Price', 'Fiat', 'Comission', 'Available', 'Asset'
         , 'minA', 'minQ','maxA','maxQ','Payment'],
    ]
    df.columns = pd.MultiIndex.from_tuples(list(zip(*columns)))
    print(df)
   

def writeRes():
    if len(rows) > 0:
        df.to_csv('pexpayP2Psell.csv')

writeRes()