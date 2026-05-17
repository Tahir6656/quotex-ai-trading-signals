# 🤖 Quotex AI Trading Signal Generator

A complete Python-based AI trading signal generator for Quotex and other trading platforms. Generate buy/sell signals using machine learning and technical indicators.

## Features

✅ **Multiple Technical Indicators**
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Moving Averages (EMA/SMA)
- Bollinger Bands
- ATR (Average True Range)

✅ **AI-Powered Signal Generation**
- Weighted indicator combination
- Confidence scoring
- Multi-indicator consensus
- Customizable signal weights

✅ **Backtesting Engine**
- Test strategies on historical data
- Performance statistics
- Win rate analysis
- Risk management

✅ **Risk Management**
- Stop-loss and take-profit levels
- Position sizing
- Risk per trade calculation

✅ **Easy Configuration**
- JSON-based settings
- Adjustable parameters
- Multiple trading pairs support

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Tahir6656/quotex-ai-trading-signals.git
cd quotex-ai-trading-signals
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the main analysis:**
```bash
python main.py
```

## Quick Start

### Generate Signals for a Symbol

```python
from data_fetcher import DataFetcher
from signals import SignalGenerator
import json

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Generate or fetch data
df = DataFetcher.generate_sample_data('EURUSD', periods=100)

# Create signal generator
signal_gen = SignalGenerator(df, config)
result = signal_gen.generate_combined_signal()

print(f"Signal: {result['signal']}")
print(f"Confidence: {result['confidence']}")
```

### Run Backtest

```python
from backtester import Backtester
from data_fetcher import DataFetcher

# Generate data
df = DataFetcher.generate_sample_data('GBPUSD', periods=200)

# Create backtester
backtester = Backtester(df, config, initial_balance=10000)
results = backtester.backtest(lookback_period=50)

# Get statistics
stats = backtester.get_statistics()
print(stats)
```

## Configuration

Edit `config.json` to customize:

```json
{
  "trading_pairs": ["EURUSD", "GBPUSD"],
  "timeframe": "5m",
  "indicators": {
    "rsi": {
      "enabled": true,
      "period": 14,
      "overbought": 70,
      "oversold": 30
    },
    "macd": {
      "enabled": true,
      "fast_period": 12,
      "slow_period": 26,
      "signal_period": 9
    }
  },
  "signal_weights": {
    "rsi": 0.25,
    "macd": 0.3,
    "moving_averages": 0.25,
    "bollinger_bands": 0.2
  },
  "min_confidence": 0.6,
  "risk_management": {
    "stop_loss_percent": 2.0,
    "take_profit_percent": 5.0,
    "max_position_size": 0.05
  }
}
```

## Project Structure

```
quotex-ai-trading-signals/
├── main.py                 # Main application
├── signals.py              # Signal generation engine
├── indicators.py           # Technical indicator calculations
├── data_fetcher.py         # Data fetching utilities
├── backtester.py           # Backtesting engine
├── config.json             # Configuration file
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
└── examples/
    └── sample_analysis.py  # Example usage
```

## Signal Types

### BUY Signal
- Multiple indicators showing upward trend
- Confidence > minimum threshold
- Price near support levels

### SELL Signal
- Multiple indicators showing downward trend
- Confidence > minimum threshold
- Price near resistance levels

### NEUTRAL Signal
- Conflicting signals from indicators
- Confidence below threshold
- Uncertain market conditions

## Examples

Run the sample analysis:
```bash
python examples/sample_analysis.py
```

This will demonstrate:
1. Basic signal generation
2. Backtesting a strategy
3. Analyzing multiple symbols

## API Data Integration

### Yahoo Finance (yfinance)

```python
from data_fetcher import DataFetcher

df = DataFetcher.fetch_from_yfinance('EURUSD', period='5d', interval='5m')
```

### CSV Files

```python
df = DataFetcher.fetch_from_csv('data.csv')
```

## Indicators Explained

### RSI (Relative Strength Index)
- Range: 0-100
- Overbought: > 70
- Oversold: < 30
- Use: Identify momentum reversal points

### MACD (Moving Average Convergence Divergence)
- Two lines: MACD and Signal
- Histogram: Difference between them
- Use: Identify trend changes and momentum

### Moving Averages
- EMA (Exponential): Responsive to recent prices
- SMA (Simple): Average of all prices
- Use: Identify trend direction

### Bollinger Bands
- Upper & Lower bands around moving average
- Use: Identify overbought/oversold conditions

## Risk Management

- **Stop Loss**: Automatic exit on loss percentage
- **Take Profit**: Automatic exit on profit percentage
- **Position Sizing**: Limit risk per trade

## Backtest Results

The backtester provides:
- Total trades executed
- Win rate percentage
- Total profit/loss
- Final balance
- Return percentage

## Important Notes

⚠️ **DISCLAIMER**: This is an educational tool for learning. Always:
- Test thoroughly before live trading
- Use with proper risk management
- Start with small position sizes
- Never risk money you can't afford to lose

## Future Enhancements

- [ ] Machine Learning models (LSTM, Random Forest)
- [ ] Real-time Quotex API integration
- [ ] Web dashboard
- [ ] Alert notifications
- [ ] Advanced portfolio analysis
- [ ] Sentiment analysis integration

## Support

For issues or questions:
1. Check the documentation
2. Review example files
3. Run the sample analysis

## License

MIT License - Feel free to use and modify

## Author

Created for learning and educational purposes.

---

**Start Trading Smarter with AI! 🚀**
