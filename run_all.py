#!/usr/bin/env python3
"""
🤖 QUOTEX AI Trading Signal Generator - ONE CLICK RUN ALL
Master file that analyzes all trading pairs and generates signals
Just double-click to run!
"""

import json
import pandas as pd
import sys
from datetime import datetime
from data_fetcher import DataFetcher
from signals import SignalGenerator
from backtester import Backtester

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_section(text):
    """Print formatted section"""
    print("\n" + "-"*70)
    print(f"  {text}")
    print("-"*70)

def load_config():
    """Load configuration from JSON"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

def analyze_symbol(symbol, config):
    """Analyze a single trading symbol"""
    print_section(f"Trading Pair: {symbol}")
    
    try:
        # Generate sample data
        print(f"\n📈 Generating data for {symbol}...")
        df = DataFetcher.generate_sample_data(symbol, periods=200)
        print(f"   ✅ Data ready: {len(df)} candles loaded")
        
        current_price = df['close'].iloc[-1]
        print(f"   💰 Current Price: {current_price:.4f}")
        
        # Validate data
        try:
            df = DataFetcher.validate_data(df)
        except ValueError as e:
            print(f"❌ Data validation error: {e}")
            return None
        
        # Generate signals
        print(f"\n🔍 Generating Trading Signals...")
        signal_gen = SignalGenerator(df, config)
        result = signal_gen.generate_combined_signal()
        print(f"   ✅ Signal Generated!")
        
        # Display signal results
        print(f"\n   📌 SIGNAL RESULT:")
        print(f"      Signal: {result['signal']}")
        print(f"      Confidence: {result['confidence']*100:.1f}%")
        print(f"      Valid: {'✅ YES' if result['is_valid'] else '❌ NO'}")
        print(f"      Buy Signals: {result['buy_signals']}")
        print(f"      Sell Signals: {result['sell_signals']}")
        
        print(f"\n   📊 INDICATOR BREAKDOWN:")
        for indicator, signal in result['details'].items():
            emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"
            print(f"      {emoji} {indicator.upper()}: {signal}")
        
        # Run backtest
        print(f"\n⏮️  Running Backtest (Testing on Historical Data)...")
        backtester = Backtester(df, config, initial_balance=10000)
        backtest_results = backtester.backtest(lookback_period=50)
        stats = backtester.get_statistics()
        print(f"   ✅ Backtest Complete!")
        
        # Display backtest stats
        print(f"\n   💹 BACKTEST STATISTICS:")
        print(f"      Starting Balance: $10,000")
        print(f"      Total Trades: {stats['total_trades']}")
        print(f"      Winning Trades: {stats.get('winning_trades', 0)}")
        print(f"      Losing Trades: {stats.get('losing_trades', 0)}")
        print(f"      Win Rate: {stats['win_rate']}%")
        print(f"      Total Profit/Loss: ${stats['total_profit']}")
        print(f"      Final Balance: ${stats['final_balance']}")
        print(f"      Return: {stats['return_percent']}%")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"results_{symbol}_{timestamp}.csv"
        backtest_results.to_csv(output_file)
        print(f"\n   📁 Backtest results saved: {output_file}")
        
        return {
            'symbol': symbol,
            'price': current_price,
            'signal': result['signal'],
            'confidence': result['confidence'],
            'is_valid': result['is_valid'],
            'stats': stats,
            'details': result['details']
        }
    
    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {e}")
        return None

def display_summary(all_results):
    """Display summary table of all pairs"""
    print_section("📋 SUMMARY TABLE - ALL PAIRS")
    
    print(f"\n{'Symbol':<12} {'Price':<15} {'Signal':<12} {'Conf%':<10} {'Trades':<8} {'Win%':<10} {'Profit':<15}")
    print("-" * 82)
    
    for result in all_results:
        if result:
            symbol = result['symbol']
            price = result['price']
            signal = result['signal']
            conf = result['confidence'] * 100
            trades = result['stats']['total_trades']
            win_rate = result['stats']['win_rate']
            profit = result['stats']['total_profit']
            
            signal_emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"
            
            print(f"{symbol:<12} {price:<15.4f} {signal_emoji} {signal:<10} {conf:<10.1f} {trades:<8} {win_rate:<10.1f} ${profit:<14.2f}")

def display_recommendations(all_results):
    """Display trading recommendations"""
    print_section("🎯 TRADING RECOMMENDATIONS")
    
    buy_signals = []
    sell_signals = []
    neutral_signals = []
    
    for result in all_results:
        if result:
            if result['signal'] == 'BUY' and result['confidence'] > 0.6:
                buy_signals.append((result['symbol'], result['confidence']))
            elif result['signal'] == 'SELL' and result['confidence'] > 0.6:
                sell_signals.append((result['symbol'], result['confidence']))
            else:
                neutral_signals.append((result['symbol'], result['confidence']))
    
    if buy_signals:
        print(f"\n🟢 STRONG BUY SIGNALS:")
        for symbol, conf in sorted(buy_signals, key=lambda x: x[1], reverse=True):
            print(f"   ✅ {symbol}: Confidence {conf*100:.1f}%")
    
    if sell_signals:
        print(f"\n🔴 STRONG SELL SIGNALS:")
        for symbol, conf in sorted(sell_signals, key=lambda x: x[1], reverse=True):
            print(f"   ✅ {symbol}: Confidence {conf*100:.1f}%")
    
    if neutral_signals:
        print(f"\n🟡 NEUTRAL (WAIT) SIGNALS:")
        for symbol, conf in sorted(neutral_signals, key=lambda x: x[1], reverse=True):
            print(f"   ⏳ {symbol}: Confidence {conf*100:.1f}%")

def display_warnings():
    """Display important trading warnings"""
    print_section("⚠️  IMPORTANT REMINDERS")
    
    warnings = [
        ("1. 🛑 ALWAYS use Stop Loss", "Set stop loss to 2% below entry price"),
        ("2. 💰 Take Profits", "Set take profit to 5% above entry price"),
        ("3. 📊 Position Sizing", "Max position size: 5% of your trading account"),
        ("4. 🧪 Backtest First", "Always test with historical data before live trading"),
        ("5. ⏰ Minimum Confidence", "Only trade signals with confidence > 60%"),
        ("6. 💡 Start Small", "Begin with small position sizes"),
        ("7. 🚫 Risk Management", "Never risk money you can't afford to lose!"),
        ("8. 🔄 Update Regularly", "Run this bot every 5-15 minutes for fresh signals"),
    ]
    
    for title, desc in warnings:
        print(f"\n  {title}")
        print(f"     → {desc}")

def save_summary(all_results):
    """Save summary to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"trading_summary_{timestamp}.txt"
    
    with open(summary_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("  🤖 QUOTEX AI TRADING SIGNAL GENERATOR - SUMMARY\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("TRADING PAIRS ANALYSIS:\n")
        f.write("-"*70 + "\n")
        
        for result in all_results:
            if result:
                f.write(f"\n{result['symbol']}:\n")
                f.write(f"  Signal: {result['signal']}\n")
                f.write(f"  Confidence: {result['confidence']*100:.1f}%\n")
                f.write(f"  Current Price: {result['price']:.4f}\n")
                f.write(f"  Valid: {'YES' if result['is_valid'] else 'NO'}\n")
                f.write(f"  Backtest Win Rate: {result['stats']['win_rate']}%\n")
                f.write(f"  Total Profit: ${result['stats']['total_profit']}\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("RECOMMENDATIONS:\n")
        f.write("="*70 + "\n")
        f.write("- Use Stop Loss: 2% below entry\n")
        f.write("- Take Profit: 5% above entry\n")
        f.write("- Max Position Size: 5% of account\n")
        f.write("- Only trade signals with confidence > 60%\n")
        f.write("- Always manage risk carefully\n")
    
    return summary_file

def main():
    """Main function"""
    print_header("🤖 QUOTEX AI TRADING SIGNAL GENERATOR")
    
    start_time = datetime.now()
    print(f"\n  Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Version: 1.0")
    
    # Load configuration
    print(f"\n📂 Loading configuration...")
    config = load_config()
    
    if not config:
        print("❌ Failed to load configuration!")
        input("Press Enter to exit...")
        return
    
    print(f"   ✅ Configuration loaded successfully!")
    
    # Get trading pairs
    trading_pairs = config.get('trading_pairs', ['EURUSD', 'GBPUSD', 'USDJPY', 'BTCUSD'])
    
    print_header(f"📊 ANALYZING {len(trading_pairs)} TRADING PAIRS")
    
    # Analyze each pair
    all_results = []
    for symbol in trading_pairs:
        result = analyze_symbol(symbol, config)
        all_results.append(result)
    
    # Display summary
    display_summary(all_results)
    
    # Display recommendations
    display_recommendations(all_results)
    
    # Display warnings
    display_warnings()
    
    # Save summary
    summary_file = save_summary(all_results)
    
    # Final message
    print_header("✅ ALL COMPLETE!")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n  Summary saved to: {summary_file}")
    print(f"  Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Duration: {duration:.1f} seconds")
    
    print(f"\n  💡 Next Steps:")
    print(f"  1. Check the generated CSV files for detailed backtest data")
    print(f"  2. Review the summary file for recommendations")
    print(f"  3. Adjust config.json if you want different settings")
    print(f"  4. Run this bot again to get fresh signals!")
    
    print("\n" + "="*70)
    print("  Press Enter to close this window...")
    print("="*70 + "\n")
    
    input()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
