import pandas as pd
import requests
from pprint import pprint
import json

def get_p2p_page_huobi(crypto_currency):
    url = 'https://www.huobi.com/-/x/otc/v1/data/trade-market?coinId=2&currency=11&tradeType=sell&currPage=1&payMethod=36,29,28&acceptOrder=0&country=&blockType=general&online=1&range=0&amount=&isThumbsUp=false&isMerchant=false&isTraded=false&onlyTradable=false&isFollowed=false'
    
    params = {
         "coinId": 2 if crypto_currency == "usdt" else (1 if crypto_currency == "btc" else 3),
        "currency": 11,
        "tradeType": "buy",
        "currPage": 0,
        "payMethod": ["29","28","36"],
        "acceptOrder": 0,
        "country": "",
        "blockType": "general",
        "online": 1,
        "range": 0,
        "amount": "",
        "isThumbsUp":False,
        "isMerchant":False,
        "isTraded": False,
        "onlyTradable": False,
        "isFollowed": False
    }
    with requests.Session() as session:
        headers = {
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        response = requests.get(url=url, headers=headers, json=params).json()
    results = response['data']
    data=[]
    for res in results:
        limit = float(res['minTradeLimit'])
        max_limit = float(res['maxTradeLimit'])
        name= res['userName']
        price=res['price']
        rate=res['orderCompleteRate']
        mounthtrade=res['tradeMonthTimes']
        CoindId=res['coinId']
        Curency=res['currency']
        tradeCount=res['tradeCount']
        payMethod=res['payMethods'][0]['name']
        UserId=res['uid']
        
       # if  limit != 20000.0 or max_limit != 200000.0:
        #    continue
        data.append([
            name,
            rate,
            mounthtrade,
            price,
            CoindId,
            Curency,
            limit,
            max_limit,
            tradeCount,
            payMethod,
            UserId])
    else:
        print("no results")
    
    columns = ['UserName','UserOrderRate','tradeMonthCount','price','coinId','CurrencyId=Rub','MinLimit','MaxLimit','TradeQuantity','payMethod','UserNumber']
    Hdf = pd.DataFrame(data,columns=columns)
    Hdf.to_csv('HuobiP2Pbuy.csv')
    print(Hdf)
    return Hdf


    

