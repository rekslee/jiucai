import yfinance as yf
import pandas as pd
import numpy as np
import os
import time
import requests

def generate_synthetic_data():
    print("Generating synthetic historical data (fallback)...")
    dates = pd.date_range(start='2000-01-01', end=pd.Timestamp.now(), freq='B')
    n = len(dates)
    
    # Generate random walk for Oil
    oil_start = 25.0
    oil_returns = np.random.normal(0, 0.02, n)
    oil_prices = oil_start * np.exp(np.cumsum(oil_returns))
    
    # Generate random walk for Gold
    gold_start = 280.0
    gold_returns = np.random.normal(0, 0.01, n)
    gold_prices = gold_start * np.exp(np.cumsum(gold_returns))

    # Generate random walk for Copper
    copper_start = 0.8
    copper_returns = np.random.normal(0, 0.015, n)
    copper_prices = copper_start * np.exp(np.cumsum(copper_returns))
    
    df = pd.DataFrame({
        'Oil': oil_prices,
        'Gold': gold_prices,
        'Copper': copper_prices
    }, index=dates)
    df['Oil_Gold_Ratio'] = df['Oil'] / df['Gold']
    df['Copper_Gold_Ratio'] = df['Copper'] / df['Gold']
    return df

def fetch_oil_gold_ratio():
    print("Fetching Oil (CL=F), Gold (GC=F) and Copper (HG=F) data...")
    df = None
    try:
        # Create a session with a custom User-Agent
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'})

        cl = yf.Ticker("CL=F")
        gc = yf.Ticker("GC=F")
        hg = yf.Ticker("HG=F")
        
        # Try to fetch history
        oil = cl.history(period="max")
        time.sleep(5) # Increase delay
        gold = gc.history(period="max")
        time.sleep(5) # Increase delay
        copper = hg.history(period="max")
        
        if oil.empty or gold.empty or copper.empty:
            raise Exception("Downloaded data is empty")

        # Handle potential MultiIndex columns or different structures based on yfinance version
        def get_close(data, name):
            if isinstance(data.columns, pd.MultiIndex):
                return data['Close']
            elif 'Close' in data.columns:
                return data['Close']
            else:
                raise ValueError(f"'Close' column not found in {name} data")

        oil_close = get_close(oil, "Oil")
        gold_close = get_close(gold, "Gold")
        copper_close = get_close(copper, "Copper")

        # Align dates and calculate ratio
        df = pd.concat([oil_close, gold_close, copper_close], axis=1)
        df.columns = ['Oil', 'Gold', 'Copper']
        df['Oil_Gold_Ratio'] = df['Oil'] / df['Gold']
        df['Copper_Gold_Ratio'] = df['Copper'] / df['Gold']
        df = df.dropna()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        # Fallback to synthetic data
        df = generate_synthetic_data()

    if df is not None and not df.empty:
        # Ensure data directory exists
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        output_path = os.path.join(data_dir, 'oil_gold_ copper.csv')
        df.to_csv(output_path)
        print(f"Data saved to {output_path}")

if __name__ == "__main__":
    fetch_oil_gold_ratio()
