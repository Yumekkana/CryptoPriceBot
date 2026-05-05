import json
import ssl
import urllib.parse
import urllib.request
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

def crypto_price(symbol):
    params = urllib.parse.urlencode(
        {
            "start": "1",
            "limit": "100",
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
        for coin in data["data"]:
            if coin["symbol"] == symbol:
                return coin["quote"]["USD"]["price"]