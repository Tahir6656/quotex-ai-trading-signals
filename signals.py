import pandas as pd
import numpy as np
from indicators import TechnicalIndicators

class SignalGenerator:
    """Generate buy/sell signals based on technical indicators"""
    
    def __init__(self, df, config):
        """
        Initialize signal generator
        df: DataFrame with OHLCV data
        config: Configuration dictionary with indicator settings
        """
        self.df = df.copy()
        self.config = config
        self.indicators_calc = TechnicalIndicators(df)
        self.indicators = self.indicators_calc.calculate_all_indicators(
            config.get('indicators', {})
        )
    
    def generate_rsi_signal(self):
        """Generate signal from RSI indicator"""
        if 'rsi' not in self.indicators:
            return None, None
        
        rsi = self.indicators['rsi']
        rsi_config = self.config['indicators']['rsi']
        oversold = rsi_config.get('oversold', 30)
        overbought = rsi_config.get('overbought', 70)
        
        current_rsi = rsi.iloc[-1]
        
        if current_rsi < oversold:
            return 'BUY', 0.8
        elif current_rsi > overbought:
            return 'SELL', 0.8
        else:
            return None, 0.3
    
    def generate_macd_signal(self):
        """Generate signal from MACD indicator"""
        if 'macd' not in self.indicators:
            return None, None
        
        macd_data = self.indicators['macd']
        macd = macd_data['macd']
        signal = macd_data['signal']
        histogram = macd_data['histogram']
        
        current_histogram = histogram.iloc[-1]
        prev_histogram = histogram.iloc[-2] if len(histogram) > 1 else None
        
        if prev_histogram is not None:
            if prev_histogram < 0 and current_histogram > 0:
                return 'BUY', 0.85
            elif prev_histogram > 0 and current_histogram < 0:
                return 'SELL', 0.85
        
        if macd.iloc[-1] > signal.iloc[-1]:
            return 'BUY', 0.6
        else:
            return 'SELL', 0.6
    
    def generate_moving_average_signal(self):
        """Generate signal from Moving Averages crossover"""
        if 'ema_short' not in self.indicators or 'ema_long' not in self.indicators:
            return None, None
        
        short_ma = self.indicators['ema_short']
        long_ma = self.indicators['ema_long']
        
        current_short = short_ma.iloc[-1]
        current_long = long_ma.iloc[-1]
        prev_short = short_ma.iloc[-2] if len(short_ma) > 1 else None
        prev_long = long_ma.iloc[-2] if len(long_ma) > 1 else None
        
        if current_short > current_long:
            confidence = 0.7
            signal = 'BUY'
        else:
            confidence = 0.7
            signal = 'SELL'
        
        return signal, confidence
    
    def generate_bollinger_bands_signal(self):
        """Generate signal from Bollinger Bands"""
        if 'bb' not in self.indicators:
            return None, None
        
        bb = self.indicators['bb']
        current_price = self.df['close'].iloc[-1]
        upper = bb['upper'].iloc[-1]
        lower = bb['lower'].iloc[-1]
        middle = bb['middle'].iloc[-1]
        
        if current_price < lower:
            return 'BUY', 0.75
        elif current_price > upper:
            return 'SELL', 0.75
        else:
            return None, 0.4
    
    def generate_combined_signal(self):
        """Generate combined signal from all enabled indicators"""
        signals = []
        confidences = []
        weights = self.config.get('signal_weights', {})
        
        # RSI Signal
        rsi_signal, rsi_conf = self.generate_rsi_signal()
        if rsi_signal:
            signals.append(rsi_signal)
            confidences.append((rsi_conf or 0.5) * weights.get('rsi', 0.25))
        
        # MACD Signal
        macd_signal, macd_conf = self.generate_macd_signal()
        if macd_signal:
            signals.append(macd_signal)
            confidences.append((macd_conf or 0.5) * weights.get('macd', 0.3))
        
        # Moving Average Signal
        ma_signal, ma_conf = self.generate_moving_average_signal()
        if ma_signal:
            signals.append(ma_signal)
            confidences.append((ma_conf or 0.5) * weights.get('moving_averages', 0.25))
        
        # Bollinger Bands Signal
        bb_signal, bb_conf = self.generate_bollinger_bands_signal()
        if bb_signal:
            signals.append(bb_signal)
            confidences.append((bb_conf or 0.5) * weights.get('bollinger_bands', 0.2))
        
        if not signals:
            return {'signal': 'NEUTRAL', 'confidence': 0, 'details': 'No signals generated'}
        
        # Count BUY vs SELL
        buy_count = signals.count('BUY')
        sell_count = signals.count('SELL')
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Determine final signal
        if buy_count > sell_count:
            final_signal = 'BUY'
        elif sell_count > buy_count:
            final_signal = 'SELL'
        else:
            final_signal = 'NEUTRAL'
        
        min_confidence = self.config.get('min_confidence', 0.6)
        is_valid = avg_confidence >= min_confidence
        
        return {
            'signal': final_signal if is_valid else 'NEUTRAL',
            'confidence': round(avg_confidence, 3),
            'is_valid': is_valid,
            'buy_signals': buy_count,
            'sell_signals': sell_count,
            'details': {
                'rsi': rsi_signal,
                'macd': macd_signal,
                'moving_average': ma_signal,
                'bollinger_bands': bb_signal
            }
        }
