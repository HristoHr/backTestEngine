# Backtest Engine

A comprehensive cryptocurrency backtesting engine for testing and optimizing trading strategies using historical market data. This project provides tools for backtesting trading algorithms, optimizing parameters using genetic algorithms, and analyzing trading performance across multiple exchanges.

## Features

- **Multiple Backtesting Engines**: Various implementations for quote-based and candle-based backtesting
- **Multi-Exchange Support**: Integration with Bitfinex, Kraken, and Coinbase Pro APIs
- **Technical Indicators**: Average True Range (ATR), Simple Moving Averages (SMA), and custom indicators
- **Genetic Algorithm Optimization**: Automated parameter optimization using GA
- **Parallel Processing**: Multi-process backtesting for faster parameter sweeps
- **Data Management**: Tools for importing, validating, and managing historical market data
- **Visualization**: Plotting capabilities for backtest results and candlestick charts

## Project Structure

### Backtesting Engines

- `backTestEngine.py` / `backTestEngine_v2.py` - Core backtesting engines for quote-based strategies
- `backTestEngineParallel.py` / `backTestEngineParallel_v2.py` - Parallelized backtesting for parameter optimization
- `candleBackTest.py` / `candleBackTest_v2.py` - Candle-based backtesting engines
- `candleBackTestEngineBTC.py` - BTC-specific candle backtesting
- `quoteBackTest.py` - Quote-level backtesting
- `quoteBackTestEngineBTC.py` / `quoteBackTestEngineFiatv2.py` - Exchange-specific quote backtesting

### Trading Logic

- `buySellLogic.py` / `buySellLogic_v2.py` - Core buy/sell decision logic implementations
- `DCLogic.py` - Donchian Channel logic (currently empty, reserved for future implementation)

### Data Acquisition

- `bitfinexAPI.py` / `bitfinexAPI_v2.py` - Bitfinex trade data API integration
- `krakenAPI.py` - Kraken exchange API integration
- `cbPro.py` - Coinbase Pro API integration using the `cbpro` library

### Data Management

- `CreateDBFormCSVs.py` - Creates SQLite databases from CSV files
- `readCSV.py` - CSV file reading utilities
- `readFromSQL.py` - SQLite database reading utilities
- `mergeTables.py` - Database table merging utilities
- `CheckDataCompletenessCSV.py` - Validates CSV data completeness
- `CheckDataCompletenessDB.py` - Validates database data completeness
- `downloadZip.py` - Utility for downloading compressed data files

### Technical Analysis

- `averageTrueRange.py` / `averageTrueRange_v2.py` - ATR calculation and analysis tools

### Optimization

- `backTestGA.py` / `backTestGA_v2.py` - Genetic algorithm for parameter optimization
- `fitnessGA.py` - Fitness function implementations for GA
- `GA.py` - Core genetic algorithm utilities (selection, crossover, mutation)
- `Example_GeneticAlgorithm.py` - Example implementation of genetic algorithm

### Visualization

- `backtestEnginePlot.py` / `backtestEnginePlot_v2.py` - Plotting utilities for backtest results using matplotlib

### Utilities

- `GenerateTestCSV.py` - Generates test CSV data
- `test.py` - General testing utilities

## Key Concepts

### Trading Strategy Parameters

The backtesting engines support various configurable parameters:

- **History Size**: Number of historical candles/periods to consider
- **Candle Size**: Time period for each candle (in minutes)
- **Profit Target**: Target profit for closing positions
- **Loss Target**: Stop-loss threshold
- **ATR Filter**: Average True Range filter for entry conditions
- **Maker/Taker Fees**: Trading fee configurations
- **Slippage**: Price slippage simulation

### Data Format

The system primarily uses SQLite databases with tables structured as:
- `quotes_EXCHANGE_ASSET`: Quote/trade data with columns (timestamp, price, volume)
- `candles_ASSET`: Candlestick data with OHLC information

## Usage Examples

### Basic Backtesting

```python
# Run a basic backtest
python backTestEngine.py
```

### Parameter Optimization with Genetic Algorithm

```python
# Optimize trading parameters using GA
python backTestGA.py
```

### Parallel Parameter Sweep

```python
# Run parallel backtests across parameter ranges
python backTestEngineParallel.py
```

### Data Import

```python
# Create database from CSV files
python CreateDBFormCSVs.py

# Fetch data from Bitfinex API
python bitfinexAPI.py

# Fetch data from Kraken API
python krakenAPI.py
```

### Visualization

```python
# Generate plots of backtest results
python backtestEnginePlot.py
```

## Dependencies

The project requires the following Python libraries:

- `sqlite3` - Database operations
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `matplotlib` - Plotting and visualization
- `requests` - HTTP requests for API calls
- `multiprocessing` - Parallel processing
- `cbpro` - Coinbase Pro API client
- `mpl_finance` - Financial plotting (candlestick charts)

## Data Sources

The engine supports historical data from:

- **Bitfinex**: Trade data via REST API
- **Kraken**: Trade data via REST API  
- **Coinbase Pro**: Market data via `cbpro` library
- **CSV Files**: Import from local CSV files

## Trading Logic

The engines implement various trading strategies:

1. **SMA-Based Strategy**: Uses Simple Moving Averages to identify entry/exit points
2. **ATR-Based Strategy**: Uses Average True Range for volatility-based entries
3. **Donchian Channel Strategy**: Uses channel breakouts (reserved for future implementation)

### Strategy Flow

1. **Data Loading**: Fetch historical data from database or CSV
2. **Candle Generation**: Convert quote data to candlestick format (if needed)
3. **Indicator Calculation**: Compute SMA, ATR, and other indicators
4. **Signal Generation**: Generate buy/sell signals based on strategy rules
5. **Trade Execution**: Simulate order execution with fees and slippage
6. **Performance Metrics**: Calculate profit, loss, win rate, and other metrics

## Performance Metrics

The backtesting engines track:

- Total profit/loss
- Profit after fees
- Win rate (profitable vs. losing trades)
- Number of trades
- Equity curve
- Trade statistics (cancelled, closed, etc.)

## Notes

- The `BmexMM/` directory contains market making related code and is excluded from this documentation
- Multiple versions (`_v2`, `_v3`) of files represent iterative improvements
- Some scripts are exchange-specific (BTC, Fiat pairs)
- Database connections use SQLite for local storage
- The genetic algorithm supports multiprocessing for faster optimization

## Contributing

When contributing to this project:

1. Ensure compatibility with existing database schemas
2. Maintain consistent parameter naming conventions
3. Add appropriate error handling for API calls
4. Include comments for complex trading logic
5. Test with historical data before deploying

## License

This project appears to be for personal/research use. Please review license requirements for any third-party APIs used.
