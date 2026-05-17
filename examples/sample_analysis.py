#!/usr/bin/env python3
"""
Sample script demonstrating how to use the trading signal generator
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from data_fetcher import DataFetcher
from signals import SignalGenerator
from backtester import Backtester

def example_1_basic_signal_generation():
    """Example 1: Generate signals for a single symbol"""
    print("\n" + "="*60)
    print("Example 1: Basic Signal Generation")
    print("="*60)
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Generate sample data
    df = DataFetcher.generate_sample_data('EURUSD', periods=100)
    
    # Create signal generator
    signal_gen = SignalGenerator(df, config)
    result = signal_gen.generate_combined_signal()
    
    print(f"Symbol: EURUSD")
    print(f"Current Price: {df['close'].iloc[-1]:.4f}")
    print(f"Signal: {result['signal']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Valid: {result['is_valid']}")

def example_2_backtest():
    """Example 2: Backtest a trading strategy"""
    print("\n" + "="*60)
    print("Example 2: Backtesting")
    print("="*60)
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Generate sample data
    df = DataFetcher.generate_sample_data('GBPUSD', periods=200)
    
    # Create backtester
    backtester = Backtester(df, config, initial_balance=10000)
    results = backtester.backtest(lookback_period=50)
    
    # Get statistics
    stats = backtester.get_statistics()
    
    print(f"\nBacktest Results for GBPUSD:")
    print(f"Total Trades: {stats['total_trades']}")
    print(f"Winning Trades: {stats.get('winning_trades', 0)}")
    print(f"Losing Trades: {stats.get('losing_trades', 0)}")
    print(f"Win Rate: {stats['win_rate']}%")
    print(f"Total Profit: ${stats['total_profit']}")
    print(f"Final Balance: ${stats['final_balance']}")
    print(f"Return: {stats['return_percent']}%")

def example_3_multiple_symbols():
    """Example 3: Analyze multiple symbols at once"""
    print("\n" + "="*60)
    print("Example 3: Multiple Symbols Analysis")
    print("="*60)
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
    
    results_summary = []
    
    for symbol in symbols:
        df = DataFetcher.generate_sample_data(symbol, periods=100)
        signal_gen = SignalGenerator(df, config)
        result = signal_gen.generate_combined_signal()
        
        results_summary.append({
            'symbol': symbol,
            'signal': result['signal'],
            'confidence': result['confidence'],
            'price': df['close'].iloc[-1]
        })
    
    print(f"\nSignals for Multiple Symbols:")
    print(f"{'-'*60}")
    print(f"{'Symbol':<12} {'Signal':<12} {'Confidence':<15} {'Price':<15}")
    print(f"{'-'*60}")
    
    for res in results_summary:
        print(f"{res['symbol']:<12} {res['signal']:<12} {res['confidence']:<15.3f} {res['price']:<15.4f}")

if __name__ == "__main__":
    print("\n🤖 Trading Signal Generator - Examples")
    
    example_1_basic_signal_generation()
    example_2_backtest()
    example_3_multiple_symbols()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")
