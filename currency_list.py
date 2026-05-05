import requests
import re


def get_currency_list(start=0, limit=20):
    url = "https://www.oanda.com/currency-converter/en/?from=USD&to=GBP&amount=1"

    headers = {
        "sec-ch-ua-platform": '"Windows"',
        "Referer": "https://www.oanda.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    html = response.text

    currencies = re.findall(
    r'\\u0022code\\u0022:\s*\\u0022(.*?)\\u0022.*?\\u0022name\\u0022:\s*\\u0022(.*?)\\u0022',
    html
    )

    currencies = list(dict.fromkeys(currencies))

    selected = currencies[start:start + limit]

    return "\n".join(f'{code}: {name}' for code, name in selected)