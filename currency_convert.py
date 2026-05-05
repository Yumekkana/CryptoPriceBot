import requests
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
beforeyesterday = today - timedelta(days=2)

def currency_converter(base, quote):
    url = f"https://fxds-public-exchange-rates-api.oanda.com/cc-api/currencies?base={base}&quote={quote}&data_type=general_currency_pair&start_date={beforeyesterday}&end_date={yesterday}"

    payload = {}
    headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://www.oanda.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    'sec-ch-ua-mobile': '?0',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    price = data['response'][0]['average_bid']
    return price