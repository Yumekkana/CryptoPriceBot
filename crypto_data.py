import json
import ssl
import urllib.parse
import urllib.request
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

def get_crypto_data():
    params = urllib.parse.urlencode(
        {
            "start": "1",
            "limit": "500",
            "convert": "USD",
        }
    )

    request = urllib.request.Request(
        f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?{params}",
        headers={
            "Accept": "application/json",
            "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAPTOKEN"),
        },
    )

    context = ssl.create_default_context(cafile=certifi.where())

    with urllib.request.urlopen(request, context=context) as response:
        data = json.load(response)
        return json.dumps(data, indent=4)
            

def get_crypto_price(symbol):
    data = get_crypto_data()
    data = json.loads(data)
    for coin in data["data"]:
        if coin["symbol"] == symbol:
            return coin["quote"]["USD"]["price"]


def get_crypto_list():
    data = get_crypto_data()
    data = json.loads(data)

    return "\n".join(
        f'{coin["name"]}: {coin["symbol"]}'
        for coin in data["data"][:20]
    )

