import requests
import re

def get_currency_list():
    url = "https://www.oanda.com/currency-converter/en/?from=USD&to=GBP&amount=1"

    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://www.oanda.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' 
    }

    response = requests.get(url, headers=headers)
    html = response.text
    match = re.findall(r'\\u0022name\\u0022:\s*\\u0022([^\\]+?)\\u0022', html)
    for currency in match[:20]:
        return currency