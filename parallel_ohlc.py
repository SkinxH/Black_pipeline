import requests
import time
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor

# === API SETTINGS ===
API_BASE = "https://pro-api.coingecko.com/api/v3"
API_KEY = "CG-q5nxd4AYP3hCaWC4GfrdRDG8"  # Replace with your API key
HEADERS = {"x-cg-pro-api-key": API_KEY}

# === TIME SETTINGS ===
START_TIMESTAMP = 1518147224  # February 9, 2018 (earliest available OHLC data)
END_TIMESTAMP = int(time.time())  # Current UNIX timestamp

# Time chunk sizes
DAILY_CHUNK = 180 * 86400  # 180 days in seconds
HOURLY_CHUNK = 31 * 86400  # 31 days in seconds

# === INPUT & OUTPUT FILES ===
INPUT_FILE = "data/coingecko_market_data.json"
PROGRESS_FILE = "data/progress_tracker.json"
DAILY_OUTPUT_FOLDER = "data/ohlc_daily/"
HOURLY_OUTPUT_FOLDER = "data/ohlc_hourly/"

# Ensure directories exist
os.makedirs(DAILY_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(HOURLY_OUTPUT_FOLDER, exist_ok=True)

# === FUNCTION TO CALL API ===
def call_endpoint(endpoint, params=None):
    """Calls a CoinGecko API endpoint and returns the JSON response."""
    url = f"{API_BASE}{endpoint}"
    try:
        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None  # Prevents crashes, allows script to retry later

# === LOAD COINS DATA ===
with open(INPUT_FILE, "r") as f:
    all_coins_data = json.load(f)

# Sort and select top 500 coins (handling NoneType for market_cap_rank)
top_500_coins = sorted(all_coins_data, key=lambda x: x["market_cap_rank"] if x["market_cap_rank"] is not None else float('inf'))[:500]
coin_ids = [coin["id"] for coin in top_500_coins]

# === LOAD OR INITIALIZE PROGRESS TRACKER ===
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        progress_tracker = json.load(f)
else:
    progress_tracker = {coin_id: {"daily": [], "hourly": []} for coin_id in coin_ids}

# === FETCH & SAVE OHLC DATA FUNCTION ===
def fetch_ohlc_data(coin_id, interval):
    """
    Fetch OHLC data for a coin in a specified interval (daily or hourly).
    Saves results incrementally to avoid losing progress.
    """
    output_folder = DAILY_OUTPUT_FOLDER if interval == "daily" else HOURLY_OUTPUT_FOLDER
    output_file = os.path.join(output_folder, f"{coin_id}.json")
    
    # Load existing data if available
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            stored_data = json.load(f)
    else:
        stored_data = []

    # Define start time (continue from last downloaded chunk)
    last_timestamp = stored_data[-1][0] if stored_data else START_TIMESTAMP
    start_time = last_timestamp

    while start_time < END_TIMESTAMP:
        end_time = min(start_time + (DAILY_CHUNK if interval == "daily" else HOURLY_CHUNK), END_TIMESTAMP)
        
        # Check if this time window has already been fetched
        if start_time in progress_tracker[coin_id][interval]:
            start_time = end_time  # Skip already downloaded chunks
            continue
        
        print(f"Fetching {interval} OHLC data for {coin_id}: {start_time} → {end_time}")

        try:
            response = call_endpoint(f"/coins/{coin_id}/ohlc/range", {
                "vs_currency": "usd",
                "from": start_time,
                "to": end_time,
                "interval": interval
            })
            
            if response:
                stored_data.extend(response)  # Append new data
                progress_tracker[coin_id][interval].append(start_time)  # Track progress
                
                # Save data incrementally
                with open(output_file, "w") as f:
                    json.dump(stored_data, f, indent=4)

                # Save progress incrementally
                with open(PROGRESS_FILE, "w") as f:
                    json.dump(progress_tracker, f, indent=4)

        except Exception as e:
            print(f"Error fetching {interval} OHLC data for {coin_id}: {e}")

        start_time = end_time  # Move to the next block
        time.sleep(0.5)  # Respect API rate limits

# === MULTI-THREADING FOR CONCURRENT REQUESTS ===
def run_parallel_requests():
    """Runs OHLC fetching in parallel using threading while respecting API limits."""
    max_threads = 5  # Adjust based on API rate limits
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        
        # Dispatch tasks for daily and hourly OHLC
        for coin_id in coin_ids:
            futures.append(executor.submit(fetch_ohlc_data, coin_id, "daily"))
            futures.append(executor.submit(fetch_ohlc_data, coin_id, "hourly"))
        
        # Wait for all threads to complete
        for future in futures:
            future.result()

# === RUN SCRIPT ===
if __name__ == "__main__":
    run_parallel_requests()
    print("\n✅ OHLC data successfully downloaded and saved.")