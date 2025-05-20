# Crypto Market Data Pipeline

This project implements a data pipeline for cryptocurrency market data, designed to feed into a Black-Litterman model. The pipeline collects, processes, and generates trading signals from various cryptocurrency data sources.

## Project Overview

The project consists of several Python scripts that work together to:
1. Fetch cryptocurrency market data from CoinGecko API
2. Process and rank cryptocurrencies by market cap
3. Generate trading signals using technical indicators
4. Collect historical OHLC (Open-High-Low-Close) data
5. Maintain up-to-date data through scheduled updates

## Project Structure

```
├── config/
│   └── config.yaml           # Configuration file for API keys and settings
├── data/
│   ├── market_caps/         # Historical market cap data
│   ├── ohlc_daily/         # Daily OHLC data
│   ├── ohlc_hourly/        # Hourly OHLC data
│   └── market_signals/     # Generated trading signals
├── src/
│   ├── data_collection/
│   │   ├── __init__.py
│   │   ├── market_data.py   # From coingecko_list.py
│   │   └── ohlc.py         # From parallel_ohlc.py
│   ├── data_processing/
│   │   ├── __init__.py
│   │   └── market_ranks.py  # From extract_market_data_with_ranks.py
│   ├── signal_generation/
│   │   ├── __init__.py
│   │   └── signals.py      # From generate_market_signals.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py       # Configuration loading
│       └── monitoring.py   # Alert and status tracking
├── scripts/
│   └── cron_jobs/
│       ├── update_market_data.py    # Hourly market data updates
│       ├── update_ohlc_daily.py     # Daily OHLC updates
│       └── update_ohlc_hourly.py    # Hourly OHLC updates
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Current Scripts Analysis

### 1. coingecko_list.py
- **Purpose**: Fetches the complete list of cryptocurrencies from CoinGecko
- **Issues**:
  - API key is hardcoded
  - No error handling for API rate limits
  - No modular structure

### 2. extract_market_data_with_ranks.py
- **Purpose**: Processes market data and calculates market cap rankings
- **Issues**:
  - File paths are hardcoded

### 3. generate_market_signals.py
- **Purpose**: Generates trading signals using EMA crossovers
- **Issues**:
  - Parameters are hardcoded
  - Signal generation logic could be modularized
  - No configuration for signal parameters

### 4. parallel_ohlc.py
- **Purpose**: Fetches historical OHLC data in parallel
- **Issues**:
  - API key is hardcoded
  (lower priority) - Progress tracking could be more robust

## Proposed Improvements

### 1. Modularization
- Split each script into smaller, focused modules
- Create a proper package structure
- Implement proper error handling and logging

### 2. Configuration Management
- Move all hardcoded values to config.yaml
- Implement environment variable support
- Add configuration validation

### 3. Data Management
- Implement proper data versioning
- Add data validation checks
- Create data backup strategy

### 4. Scheduling System
- Implement proper cron job management
- Add job status monitoring
- Create failure recovery mechanisms

## Next Steps

1. **Project Restructuring**
   - Create the proposed directory structure
   - Move existing code into appropriate modules
   - Implement proper package management

2. **Configuration System**
   - Create config.yaml template
   - Implement configuration loading system
   - Add environment variable support

3. **Data Pipeline Improvements**
   - Implement proper error handling
   - Add data validation
   - Create data backup system

4. **Scheduling System**
   - Create cron job scripts
   - Implement monitoring system
   - Add alerting for failures

5. **Documentation**
   - Add detailed API documentation
   - Create setup instructions
   - Add usage examples

## Requirements

The project will require:
- Python 3.8+
- CoinGecko Pro API key
- Sufficient storage for historical data
- Regular backup system
- Monitoring system for cron jobs

## Future Integration with Black-Litterman Model

The current pipeline is designed to feed into a Black-Litterman model. Future work will include:
1. Signal aggregation and normalization
2. Risk factor calculation
3. Portfolio optimization integration
4. Backtesting framework
5. Performance monitoring system 

## Cron Job Details

### 1. Market Data Updates
- **Script**: `scripts/cron_jobs/update_market_data.py`
- **Schedule**: `0 * * * *` (Every hour at minute 0)
- **Purpose**: Updates current market data, rankings, and generates signals
- **Dependencies**: None
- **Expected runtime**: 5-10 minutes

### 2. Daily OHLC Updates
- **Script**: `scripts/cron_jobs/update_ohlc_daily.py`
- **Schedule**: `0 0 * * *` (Every day at midnight)
- **Purpose**: Updates daily OHLC data for all tracked coins
- **Dependencies**: None
- **Expected runtime**: 15-30 minutes

### 3. Hourly OHLC Updates
- **Script**: `scripts/cron_jobs/update_ohlc_hourly.py`
- **Schedule**: `30 * * * *` (Every hour at minute 30)
- **Purpose**: Updates hourly OHLC data for all tracked coins
- **Dependencies**: None
- **Expected runtime**: 10-15 minutes

### 4. New Files to Create
1. **src/utils/config.py**
   - Configuration loading
   - Environment variable handling
   - Configuration validation
   - Path management

2. **src/utils/monitoring.py**
   - Alert system
   - Status tracking
   - Failure recovery
   - Performance monitoring

3. **scripts/cron_jobs/update_market_data.py**
   - Market data updates
   - Signal generation
   - Status reporting
   - Error handling

4. **scripts/cron_jobs/update_ohlc_daily.py**
   - Daily OHLC updates
   - Progress tracking
   - Error recovery
   - Status reporting

5. **scripts/cron_jobs/update_ohlc_hourly.py**
   - Hourly OHLC updates
   - Progress tracking
   - Error recovery
   - Status reporting

### 5. Cron Job Implementation Details
Each cron job should:
1. Load configuration
2. Set up logging
3. Check for running instances
4. Execute the update
5. Handle errors
6. Send status reports
7. Clean up temporary files
8. Update progress tracking

The jobs should be staggered to avoid API rate limits:
- Market data: 00:00
- Hourly OHLC: 00:30
- Daily OHLC: 01:00

Each job should also implement:
- Lock files to prevent concurrent runs
- Progress tracking
- Error recovery
- Alert system integration
- Log rotation
- Data validation
- Backup creation

