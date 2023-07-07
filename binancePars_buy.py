import pandas as pd
import requests
import json

def get_p2p_page(crypto_currency):
  
    json_data = {
        "page":0,
        "rows":200,
        "asset":crypto_currency,
        "fiat":"RUB",
        "payTypes": ["TinkoffNew","RosBankNew","RaiffeisenBank"],
        "tradeType":"BUY"
    }
    with requests.Session() as session:
        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        
        response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=json_data)
        
        results=response.json()['data']
        print(results)
        data = []
        for res in results:
            limit = float(res['adv']['minSingleTransAmount'])
            max_limit = float(res['adv']['dynamicMaxSingleTransAmount'])
            price=res['adv']['price']
            nickname=res['advertiser']['nickName']
            mtOrderCount=res['advertiser']['monthOrderCount']
            mtRate=res['advertiser']['monthFinishRate']
            fiat=res['adv']['fiatUnit']
            asset=res['adv']['asset']
            commision=res['adv']['commissionRate']
            quantity=res['adv']['tradableQuantity']
            payment=res['adv']['tradeMethods'][0]['tradeMethodName']
            userno=res['advertiser']['userNo']


            if limit != 100000.0 or max_limit != 500000.0:
                continue
            data.append([
                nickname,
                mtOrderCount,
                mtRate,
                price,
                fiat,
                commision,
                quantity,
                asset,
                limit,
                max_limit,
                payment,
                userno])

        else:
            print('no result')
   
            columns = [
        ['Advertisers (completion rate)']*3 + ['Price']*3 + ['Available']*2 + ['Limit Amount & Quantity']*4 + ['']*2,
        ['Name', 'Orders', 'Completion', 'Price', 'Fiat', 'Comission', 'Available', 'Asset'
         , 'minA','maxA','Payment','advertiserNo'],
    ]
            df = pd.DataFrame(data,columns=columns)
            print(df)
            df.to_csv('binanceP2Pbuy.csv')
            return df
            print('https://p2p.binance.com/en/advertiserDetail?advertiserNo=' + df.iloc[0,-1])
       






get_p2p_page("USDT")
