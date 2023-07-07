import pandas as pd
import requests


def get_bybit_prices_sell(crypto_currency):
    url = 'https://api2.bybit.com/fiat/otc/item/online'
    params = {
        "userId": "",
        "tokenId": crypto_currency,
        "currencyId": "RUB",
        "payment": ["64", "75", "377"],
        "side": "0",
        "size": "100",  # изменяем размер страницы
        "page": "0",
        "amount": "",
        "authMaker": False,
        "canTrade": False
    }
    with requests.Session() as session:
        headers = {
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        response = requests.post(url=url, headers=headers, json=params).json()
    results = response['result']['items']
    data = []
    for res in results:
        sell_min_lim = float(res['minAmount'])
        sell_max_lim = float(res['maxAmount'])
        USdt_price_sell = res['price']
        buyer_name = res['nickName']
        buyer_rate = res['recentExecuteRate']
        bueyr_order_count = res['recentOrderNum']
        sell_paytype = res['payments'][0]
        #if sell_min_lim != 20000.0 or sell_max_lim != 3500000.0:
         #   continue    
        data.append([
                USdt_price_sell,
                buyer_name,
                buyer_rate,
                bueyr_order_count,
                sell_paytype,
                sell_min_lim,
                sell_max_lim
            ])
    else:
        print('no result')

    
    columns = ['price', 'Buyer Name', 'Buyer Rate', 'Seller Order Count', 'SEll Payment Type', 'Sell Min Limit', 'Sell Max Limit']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('bybitP2Psell.csv') 
    print(df)
    return df



