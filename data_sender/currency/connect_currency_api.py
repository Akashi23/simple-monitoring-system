import requests
import json


def request_to_currency_api():
    API_KEY = '270f05d62db34ddcba9a57c65b092d44'

    url = f'https://api.currencyfreaks.com/latest?apikey={API_KEY}'

    headers = {}

    response = requests.request("GET", url, headers=headers)
    return response.text

def request_to_btc_api():

    url = f'https://blockchain.info/ticker'

    headers = {}

    response = requests.request("GET", url, headers=headers)
    return response.text

def save_to_influxdb_currency():
    btc_api = json.loads(request_to_btc_api())
    currency_api = json.loads(request_to_currency_api())

    all_api = {
        'measurement': 'currency',
        'time': currency_api['date']
    }

    all_api['tags'] = {
        'base' : 'KZT'
    }

    all_api['fields'] = {
        'USD' : float(currency_api['rates']['KZT']),
        'EUR' : float(currency_api['rates']['KZT']) / float(currency_api['rates']['EUR']),
        'RUB' : float(currency_api['rates']['KZT']) / float(currency_api['rates']['RUB']),
        'BTC' : float(btc_api['USD']['last']) * float(currency_api['rates']['KZT'])
    }

    return all_api


    

if __name__ == "__main__":
    print(save_to_influxdb_currency())