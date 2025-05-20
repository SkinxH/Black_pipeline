import requests
import time
import json

API_BASE = "https://pro-api.coingecko.com/api/v3"
API_KEY = "CG-q5nxd4AYP3hCaWC4GfrdRDG8"
HEADERS = {"x-cg-pro-api-key": API_KEY}

def call_endpoint(endpoint, params=None):
    """Calls a CoinGecko API endpoint and returns the response as JSON."""
    url = f"{API_BASE}{endpoint}"
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

# 1. Get the full coin list with market data
all_coins_data = []
page = 1
while True:
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": page
    }
    data = call_endpoint("/coins/markets", params)
    if not data:
        break
    all_coins_data.extend(data)
    if len(data) < 250:
        break
    page += 1
    time.sleep(1)  # To respect API rate limits

# 2. Save the data to a JSON file
output_file = "coingecko_market_data.json"
with open(output_file, "w") as f:
    json.dump(all_coins_data, f, indent=4)

print(f"Data successfully saved to {output_file}")
