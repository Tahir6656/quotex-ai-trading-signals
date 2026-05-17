import json
import pandas as pd
from data_fetcher import DataFetcher
from signals import SignalGenerator
from backtester import Backtester

def load_config(config_file='config.json'):
    """Load configuration from JSON file"""
    with open(config_file, 'r') as f:
        return json.load(f)

def analyze_symbol(symbol, df, config):
    """Analyze a single trading symbol"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {symbol}")
    print(f"{'='*60}")
    
    # Generate signals
    signal_gen = SignalGenerator(df, config)
    result = signal_gen.generate_combined_signal()
    
    # Display results
    print(f"Signal: {result['signal']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Is Valid: {result['is_valid']}")
    print(f"\nSignal Details:")
    for indicator, signal in result['details'].items():
        print(f"  {indicator}: {signal}")
    
    return result

def backtest_symbol(symbol, df, config):
    """Run backtest on a symbol"""
    print(f"\nBacktesting {symbol}...")
    
    backtester = Backtester(df, config)
    backtest_results = backtester.backtest(lookback_period=50)
    stats = backtester.get_statistics()
    
    print(f"\nBacktest Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return backtest_results, stats

def main():
    """Main function"""
    # Load configuration
    config = load_config()
    
    print("\n🤖 Quotex AI Trading Signal Generator")
    print("="*60)
    
    # Analyze each trading pair
    for symbol in config['trading_pairs']:
        print(f"\nFetching data for {symbol}...")
        
        # For demo purposes, we'll use sample data
        # In production, you would use real API data
        df = DataFetcher.generate_sample_data(symbol, periods=200)
        
        # Validate data
        try:
            df = DataFetcher.validate_data(df)
        except ValueError as e:
            print(f"Error: {e}")
            continue
        
        # Analyze current signals
        analyze_symbol(symbol, df, config)
        
        # Run backtest
        backtest_results, stats = backtest_symbol(symbol, df, config)
        
        # Save results
        output_file = f"results_{symbol}.csv"
        backtest_results.to_csv(output_file)
        print(f"\n✅ Results saved to {output_file}")
    
    print(f"\n{'='*60}")
    print("Analysis complete!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
