import pandas as pd
import numpy as np
from signals import SignalGenerator
from data_fetcher import DataFetcher

class Backtester:
    """Backtest trading signals on historical data"""
    
    def __init__(self, df, config, initial_balance=10000):
        """
        Initialize backtester
        df: DataFrame with OHLCV data
        config: Configuration dictionary
        initial_balance: Starting balance for simulation
        """
        self.df = df.copy()
        self.config = config
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.trades = []
        self.position = None  # Current position: BUY or SELL
        self.entry_price = None
    
    def backtest(self, lookback_period=50):
        """
        Run backtest on historical data
        lookback_period: Number of candles to look back for indicators
        """
        results = []
        
        for i in range(lookback_period, len(self.df)):
            # Get data up to current point
            data_slice = self.df.iloc[:i+1]
            current_price = data_slice['close'].iloc[-1]
            current_date = data_slice.index[-1]
            
            # Generate signal
            signal_gen = SignalGenerator(data_slice, self.config)
            signal_result = signal_gen.generate_combined_signal()
            
            # Process signal
            signal = signal_result['signal']
            confidence = signal_result['confidence']
            
            trade_result = self.process_signal(
                signal, confidence, current_price, current_date, signal_result
            )
            
            results.append({
                'date': current_date,
                'price': current_price,
                'signal': signal,
                'confidence': confidence,
                'balance': self.balance,
                'position': self.position,
                'trade': trade_result
            })
        
        return pd.DataFrame(results)
    
    def process_signal(self, signal, confidence, price, date, signal_details):
        """
        Process trading signal and execute trades
        """
        trade = None
        min_conf = self.config.get('min_confidence', 0.6)
        
        if confidence < min_conf:
            return None
        
        if signal == 'BUY' and self.position is None:
            # Enter long position
            position_size = self.calculate_position_size(price)
            self.position = 'LONG'
            self.entry_price = price
            self.balance -= position_size * price
            
            trade = {
                'type': 'BUY',
                'date': date,
                'price': price,
                'size': position_size,
                'confidence': confidence
            }
            self.trades.append(trade)
        
        elif signal == 'SELL' and self.position == 'LONG':
            # Exit long position
            position_size = self.calculate_position_size(price)
            profit_loss = (price - self.entry_price) * position_size
            self.balance += position_size * price + profit_loss
            
            trade = {
                'type': 'SELL',
                'date': date,
                'price': price,
                'size': position_size,
                'profit_loss': profit_loss,
                'confidence': confidence
            }
            self.trades.append(trade)
            self.position = None
            self.entry_price = None
        
        return trade
    
    def calculate_position_size(self, current_price):
        """
        Calculate position size based on risk management rules
        """
        max_position = self.config.get('risk_management', {}).get('max_position_size', 0.05)
        position_size = (self.balance * max_position) / current_price
        return max(position_size, 0.1)  # Minimum 0.1 units
    
    def get_statistics(self):
        """
        Calculate backtest statistics
        """
        if not self.trades:
            return {'total_trades': 0, 'win_rate': 0, 'total_profit': 0}
        
        profit_loss_trades = [t for t in self.trades if 'profit_loss' in t]
        
        if not profit_loss_trades:
            return {'total_trades': len(self.trades), 'win_rate': 0, 'total_profit': 0}
        
        wins = sum(1 for t in profit_loss_trades if t['profit_loss'] > 0)
        losses = sum(1 for t in profit_loss_trades if t['profit_loss'] < 0)
        total_profit = sum(t.get('profit_loss', 0) for t in profit_loss_trades)
        win_rate = wins / len(profit_loss_trades) if profit_loss_trades else 0
        
        return {
            'total_trades': len(profit_loss_trades),
            'winning_trades': wins,
            'losing_trades': losses,
            'win_rate': round(win_rate * 100, 2),
            'total_profit': round(total_profit, 2),
            'final_balance': round(self.balance, 2),
            'return_percent': round((self.balance - self.initial_balance) / self.initial_balance * 100, 2)
        }
