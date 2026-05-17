import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, MACD
from ta.trend import EMAIndicator, SMAIndicator
from ta.volatility import BollingerBands

class TechnicalIndicators:
    """Calculate technical indicators for trading signals"""
    
    def __init__(self, df):
        """
        Initialize with OHLCV data
        df: DataFrame with columns ['open', 'high', 'low', 'close', 'volume']
        """
        self.df = df.copy()
        self.df = self.df.reset_index(drop=True)
    
    def calculate_rsi(self, period=14):
        """Calculate Relative Strength Index"""
        rsi = RSIIndicator(close=self.df['close'], window=period)
        return rsi.rsi()
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        macd = MACD(close=self.df['close'], window_fast=fast, window_slow=slow, window_sign=signal)
        return {
            'macd': macd.macd(),
            'signal': macd.macd_signal(),
            'histogram': macd.macd_diff()
        }
    
    def calculate_ema(self, period=20):
        """Calculate Exponential Moving Average"""
        ema = EMAIndicator(close=self.df['close'], window=period)
        return ema.ema_indicator()
    
    def calculate_sma(self, period=20):
        """Calculate Simple Moving Average"""
        sma = SMAIndicator(close=self.df['close'], window=period)
        return sma.sma_indicator()
    
    def calculate_bollinger_bands(self, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        bb = BollingerBands(close=self.df['close'], window=period, window_dev=std_dev)
        return {
            'upper': bb.bollinger_hband(),
            'middle': bb.bollinger_mavg(),
            'lower': bb.bollinger_lband()
        }
    
    def calculate_atr(self, period=14):
        """Calculate Average True Range for volatility"""
        high_low = self.df['high'] - self.df['low']
        high_close = np.abs(self.df['high'] - self.df['close'].shift())
        low_close = np.abs(self.df['low'] - self.df['close'].shift())
        
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
    
    def calculate_all_indicators(self, config):
        """Calculate all enabled indicators from config"""
        indicators = {}
        
        if config.get('rsi', {}).get('enabled'):
            period = config['rsi'].get('period', 14)
            indicators['rsi'] = self.calculate_rsi(period)
        
        if config.get('macd', {}).get('enabled'):
            fast = config['macd'].get('fast_period', 12)
            slow = config['macd'].get('slow_period', 26)
            signal = config['macd'].get('signal_period', 9)
            indicators['macd'] = self.calculate_macd(fast, slow, signal)
        
        if config.get('moving_averages', {}).get('enabled'):
            short = config['moving_averages'].get('short_period', 20)
            long = config['moving_averages'].get('long_period', 50)
            indicators['ema_short'] = self.calculate_ema(short)
            indicators['ema_long'] = self.calculate_ema(long)
        
        if config.get('bollinger_bands', {}).get('enabled'):
            period = config['bollinger_bands'].get('period', 20)
            std = config['bollinger_bands'].get('std_dev', 2)
            indicators['bb'] = self.calculate_bollinger_bands(period, std)
        
        return indicators
