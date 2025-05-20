import pandas as pd
import numpy as np
import os

EMA_SHORT = 13
EMA_LONG = 21
DECAY_FACTOR = 0.97 
MARKET_DATA_FILE = 'data/market_data_with_ranks.csv'

def main():
    print(f"Loading market data from {MARKET_DATA_FILE}...")
    
    # Check if the file exists
    if not os.path.exists(MARKET_DATA_FILE):
        print(f"Error: {MARKET_DATA_FILE} not found. Please run extract_market_data_with_ranks.py first.")
        return
    
    # Read the CSV into a DataFrame
    data = pd.read_csv(MARKET_DATA_FILE)
    
    # Convert date to datetime
    data['time_bucket'] = pd.to_datetime(data['date'])
    
    # Rename columns
    data = data.rename(columns={
        'price': 'close'
    })
    
    # Create pair column using symbol
    data['pair'] = data.apply(lambda row: f"{row['symbol']}/USD", axis=1)
    
    # Add quote column
    data['quote'] = 'USD'
    data['base'] = data['symbol'] 
    
    # Ensure data is sorted by pair and time
    data = data.sort_values(by=['pair', 'time_bucket'])
    
    print(f"Processing {data['coin_id'].nunique()} coins...")
    
    all_signals = []
    
    # Process each pair separately
    for pair, df_asset in data.groupby('pair'):
        df = df_asset.copy().reset_index(drop=True)
        
        # Calculate EMAs
        df['ema_short'] = df['close'].ewm(span=EMA_SHORT, adjust=False).mean()
        df['ema_long'] = df['close'].ewm(span=EMA_LONG, adjust=False).mean()
        
        # Default signal is 0
        df['signal'] = 0
        
        # Identify buy signals (crossover up)
        buy_signals = (df['ema_short'] > df['ema_long']) & (df['ema_short'].shift(1) <= df['ema_long'].shift(1))
        df.loc[buy_signals, 'signal'] = 1
        
        # Identify sell signals (crossover down)
        sell_signals = (df['ema_short'] < df['ema_long']) & (df['ema_short'].shift(1) >= df['ema_long'].shift(1))
        df.loc[sell_signals, 'signal'] = -1
        
        # Check base asset: stablecoins should have no signals
        base_asset = df['symbol'].iloc[0].lower()
        
        if base_asset in ['usdt', 'usdc', 'usd', 'dai', 'busd', 'tusd']:
            df['signal'] = 0
        else:
            # Maintain persistent state
            current_state = 0
            for i in range(len(df)):
                if df.at[i, 'signal'] == 1:
                    current_state = 1
                elif df.at[i, 'signal'] == -1:
                    current_state = -1
                else:
                    df.at[i, 'signal'] = current_state
            
            # Calculate days since last signal change
            prev_signal = 0
            days_since = 0
            for i in range(len(df)):
                current_signal = df.at[i, 'signal']
                if current_signal == 0:
                    days_since = 0
                else:
                    if current_signal != prev_signal and prev_signal != 0:
                        days_since = 0
                    elif current_signal == prev_signal:
                        days_since += 1
                    else:
                        days_since = 0  # Transition from 0 to signal
                df.at[i, 'days_since'] = days_since
                prev_signal = current_signal
            
            # Apply time decay
            df['signal'] = df['signal'] * (DECAY_FACTOR ** df['days_since'])
            df['signal'] = df['signal'].round(3)
        
        # Select columns
        all_signals.append(df[['time_bucket', 'pair', 'base', 'quote', 'close', 'signal', 'market_cap', 'market_cap_rank', 'coin_id', 'symbol']])
    
    # Combine all signals
    final_df = pd.concat(all_signals, ignore_index=True)
    
    # Save to CSV
    output_file = 'data/market_signals.csv'
    final_df.to_csv(output_file, index=False)
    print(f"Market signals generated and saved to {output_file}")
    
    # Create a summary of the latest signals
    latest_date = final_df['time_bucket'].max()
    latest_signals = final_df[final_df['time_bucket'] == latest_date].copy()
    latest_signals = latest_signals.sort_values('market_cap_rank')
    
    latest_file = 'data/latest_market_signals.csv'
    latest_signals.to_csv(latest_file, index=False)
    print(f"Latest signals as of {latest_date} saved to {latest_file}")
    
    # Print statistics
    buy_signals = latest_signals[latest_signals['signal'] > 0]
    sell_signals = latest_signals[latest_signals['signal'] < 0]
    neutral_signals = latest_signals[latest_signals['signal'] == 0]
    
    print(f"\nSignal Summary for {latest_date.date()}:")
    print(f"Buy signals: {len(buy_signals)} coins")
    print(f"Sell signals: {len(sell_signals)} coins")
    print(f"Neutral signals: {len(neutral_signals)} coins")
    
    # Print top 10 buy and sell signals by market cap
    if len(buy_signals) > 0:
        print("\nTop Buy Signals (by market cap):")
        top_buys = buy_signals.sort_values('market_cap_rank').head(10)
        for _, row in top_buys.iterrows():
            print(f"{row['symbol']}: Signal = {row['signal']:.3f}, Rank = {row['market_cap_rank']}")
    
    if len(sell_signals) > 0:
        print("\nTop Sell Signals (by market cap):")
        top_sells = sell_signals.sort_values('market_cap_rank').head(10)
        for _, row in top_sells.iterrows():
            print(f"{row['symbol']}: Signal = {row['signal']:.3f}, Rank = {row['market_cap_rank']}")

if __name__ == "__main__":
    main() 