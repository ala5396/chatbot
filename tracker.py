import requests


def get_prices():
    coins = ["BTC", "ETH", "XRP", "LTC", "BCH",
             "ADA", "DOT", "LINK", "BNB", "XLM"]

    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD".format(",".join(coins))).json()["RAW"]

    data = {}
    for i in crypto_data:
        data[i] = {
            "coin": i,
            "price": crypto_data[i]["USD"]["PRICE"],
            "change_day": crypto_data[i]["USD"]["CHANGEPCT24HOUR"],
            "change_hour": crypto_data[i]["USD"]["CHANGEPCTHOUR"]
        }

    return data


def get_volume(mint, coin1, coin2):
    e = ['Bitfinex', 'Bibox', 'Binance', 'Bittrex']

    time_data = requests.get(
        "https://min-api.cryptocompare.com/data/v2/histominute?fsym={}&tsym={}&limit={}&e={}".format(coin1, coin2, mint, ",".join(e))).json()

    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/generateAvg?fsym={}&tsym={}&e={}".format(coin1, coin2, ",".join(e))).json()
    data = {}

    data['time'] = round(time_data['Data']['Data'][mint-1]['volumeto'] -
                         time_data['Data']['Data'][0]['volumeto'])
    data['p'] = round(time_data['Data']['Data'][mint-1]['close'] -
                      time_data['Data']['Data'][0]['close'])
    data['vol'] = round(crypto_data['RAW']['VOLUME24HOURTO'])
    data['vol_p'] = data['time'] / data['vol'] * 100
    data['price'] = round(crypto_data['RAW']['PRICE'])
    data['price_p'] = data['p'] / data['price'] * 100
    data['LM'] = crypto_data['RAW']['LASTMARKET']
    return data


if __name__ == "__main__":
    print(get_prices())
