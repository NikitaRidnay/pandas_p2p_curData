import pandas as pd
import requests


def get_bybit_prices(crypto_currency):
    url = 'https://api2.bybit.com/fiat/otc/item/online'
    params = {
        "userId": "",
        "tokenId": crypto_currency,
        "currencyId": "RUB",
        "payment": ["64", "75", "377"],
        "side": "1",
        "size": "300",  # изменяем размер страницы
        "page": "1",
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
        buy_min_lim = float(res['minAmount'])
        buy_max_lim = float(res['maxAmount'])
        USdt_price_buy = res['price']
        Seller_name = res['nickName']
        Seller_rate = res['recentExecuteRate']
        Seller_order_count = res['recentOrderNum']
        buy_paytype = res['payments'][0]
        #if buy_min_lim != 20000.0 or buy_max_lim != 3500000.0:
         #   continue    
        data.append([
                USdt_price_buy,
                Seller_name,
                Seller_rate,
                Seller_order_count,
                buy_paytype,
                buy_min_lim,
                buy_max_lim
            ])
    else:
        print('no result')

    
    columns = ['price', 'Seller Name', 'Seller Rate', 'Seller Order Count', 'Buy Payment Type', 'Buy Min Limit', 'Buy Max Limit']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('bybitP2Pbuy2.csv') 
    print(df)
    return df

get_bybit_prices("USDT")

