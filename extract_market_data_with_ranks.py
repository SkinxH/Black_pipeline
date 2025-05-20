import os
import json
import csv
import glob
import pandas as pd
from datetime import datetime

def convert_timestamp_to_date(timestamp_ms):
    """Convert millisecond timestamp to a date string in YYYY-MM-DD format."""
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d')

def load_coin_symbols():
    """Load coin symbols from coingecko_market_data.json."""
    try:
        with open('data/coingecko_market_data.json', 'r', encoding='utf-8') as f:
            coingecko_data = json.load(f)
        
        # Create a dictionary mapping coin_id to symbol
        symbols_dict = {}
        for coin in coingecko_data:
            if 'id' in coin and 'symbol' in coin:
                symbols_dict[coin['id']] = coin['symbol'].upper()
        
        print(f"Loaded {len(symbols_dict)} coin symbols from coingecko_market_data.json")
        return symbols_dict
    
    except Exception as e:
        print(f"Error loading coin symbols: {str(e)}")
        #  load the file in chunks if it's too large
        try:
            symbols_dict = {}
            with open('data/coingecko_market_data.json', 'r', encoding='utf-8') as f:
                # Read the file line by line
                data_str = ""
                for line in f:
                    data_str += line
                    if "}" in line and "," in line:
                        #  parse this chunk as a JSON object
                        try:
                            coin = json.loads(data_str.strip().rstrip(','))
                            if isinstance(coin, dict) and 'id' in coin and 'symbol' in coin:
                                symbols_dict[coin['id']] = coin['symbol'].upper()
                            data_str = ""
                        except:
                            # If parsing fails, continue accumulating lines
                            pass
            
            if symbols_dict:
                print(f"Loaded {len(symbols_dict)} coin symbols using alternative method")
                return symbols_dict
        except Exception as inner_e:
            print(f"Error in alternative loading method: {str(inner_e)}")
        
        return {}

def extract_data_from_json(json_file, symbols_dict):
    """Extract price and market cap data from a single JSON file."""
    coin_id = os.path.basename(json_file).replace('.json', '')
    symbol = symbols_dict.get(coin_id, coin_id.upper())  
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        combined_data = []
        
        # Extract both price and market cap data
        if ('prices' in data and isinstance(data['prices'], list) and 
            'market_caps' in data and isinstance(data['market_caps'], list)):
            
            # Create dictionaries for faster lookups
            price_dict = {entry[0]: entry[1] for entry in data['prices'] if len(entry) == 2}
            mcap_dict = {entry[0]: entry[1] for entry in data['market_caps'] if len(entry) == 2}
            
            # Find common timestamps
            common_timestamps = set(price_dict.keys()).intersection(set(mcap_dict.keys()))
            
            for timestamp_ms in common_timestamps:
                date_str = convert_timestamp_to_date(timestamp_ms)
                price = price_dict.get(timestamp_ms)
                market_cap = mcap_dict.get(timestamp_ms)
                if price is not None and market_cap is not None:
                    combined_data.append((date_str, coin_id, symbol, price, market_cap))
        
        return combined_data
    
    except Exception as e:
        print(f"Error processing {coin_id}: {str(e)}")
        return []

def main():
    # Load coin symbols
    symbols_dict = load_coin_symbols()
    
    # Get list of all JSON files in market_caps directory
    json_files = glob.glob('data/market_caps/*.json')
    
    all_combined_data = []
    
    print(f"Found {len(json_files)} JSON files to process.")
    
    # Process each JSON file
    for i, json_file in enumerate(json_files):
        if i % 10 == 0:
            print(f"Processing file {i+1}/{len(json_files)}: {os.path.basename(json_file)}")
        
        combined_data = extract_data_from_json(json_file, symbols_dict)
        all_combined_data.extend(combined_data)
    
    print(f"Extracted {len(all_combined_data)} combined data points.")
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(all_combined_data, columns=['date', 'coin_id', 'symbol', 'price', 'market_cap'])
    
    # Calculate market cap rank for each date
    print("Calculating market cap ranks...")
    df['market_cap_rank'] = df.groupby('date')['market_cap'].rank(ascending=False, method='min').astype(int)
    
    # Sort by date and rank
    df = df.sort_values(['date', 'market_cap_rank'])
    
    # Write data to CSV
    combined_csv_path = 'data/market_data_with_ranks.csv'
    df.to_csv(combined_csv_path, index=False)
    
    print(f"Combined market data with ranks saved to {combined_csv_path}")
    print(f"Total coins: {df['coin_id'].nunique()}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total records: {len(df)}")
    
    # Create a filtered dataset with only top N coins by market cap
    top_n = 100  
    df_top = df[df['market_cap_rank'] <= top_n].copy()
    top_path = f'data/top{top_n}_market_data.csv'
    df_top.to_csv(top_path, index=False)
    print(f"Created filtered dataset with only top {top_n} coins by market cap: {top_path}")

if __name__ == "__main__":
    main() 