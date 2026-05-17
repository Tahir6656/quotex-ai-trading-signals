import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import json

class DataFetcher:
    """Fetch trading data from various sources"""
    
    @staticmethod
    def generate_sample_data(symbol, periods=100, start_price=100):
        """
        Generate sample OHLCV data for testing
        Useful for backtesting without API access
        """
        np.random.seed(42)
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='5min')
        
        prices = [start_price]
        for _ in range(periods - 1):
            change = np.random.normal(0, 1)
            new_price = prices[-1] * (1 + change / 100)
            prices.append(max(new_price, 1))  # Prevent negative prices
        
        data = []
        for i, date in enumerate(dates):
            base_price = prices[i]
            open_p = base_price
            high = base_price * (1 + abs(np.random.normal(0, 0.5)) / 100)
            low = base_price * (1 - abs(np.random.normal(0, 0.5)) / 100)
            close = base_price * (1 + np.random.normal(0, 0.3) / 100)
            volume = np.random.randint(1000, 10000)
            
            data.append({
                'timestamp': date,
                'open': open_p,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        return df
    
    @staticmethod
    def fetch_from_yfinance(symbol, period='5d', interval='5m'):
        """
        Fetch real data from Yahoo Finance (if available for the symbol)
        """
        try:
            import yfinance as yf
            data = yf.download(symbol, period=period, interval=interval, progress=False)
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            return data
        except Exception as e:
            print(f"Error fetching from Yahoo Finance: {e}")
            return None
    
    @staticmethod
    def fetch_from_csv(filepath):
        """
        Load trading data from CSV file
        Expected columns: timestamp, open, high, low, close, volume
        """
        try:
            df = pd.read_csv(filepath)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None
    
    @staticmethod
    def validate_data(df):
        """
        Validate that dataframe has required columns
        """
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing = [col for col in required_columns if col not in df.columns]
        
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        
        # Check for NaN values
        if df[required_columns].isnull().any().any():
            print("Warning: NaN values found, dropping rows with NaN")
            df = df.dropna()
        
        return df
