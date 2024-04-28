import os
import time
import yfinance as yf
import pandas as pd

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_data(tickers, interval):
    # Adjust directory mapping to include hourly data
    directory_mapping = {
        '1d': 'DAILY',
        '1wk': 'WEEKLY',
        '1mo': 'MONTHLY',
        '1h': 'HOURLY'  # New entry for hourly data
    }
    # Adjust the period for downloading data based on interval
    period_mapping = {
        '1d': '1y',
        '1wk': '1y',
        '1mo': '1y',
        '1h': '1wk'  # Use one (1wk)week / (1mo)month for hourly data
    }
    data_dir = directory_mapping[interval]
    ensure_directory_exists(data_dir)

    for ticker in tickers:
        print(f"Downloading {interval} data for {ticker}")
        period = period_mapping[interval]
        data = yf.download(ticker, period=period, interval=interval)
        filename = os.path.join(data_dir, f"{ticker}.csv")
        data.to_csv(filename)
        print(f"Saved {interval} data for {ticker} to {filename}")
        time.sleep(1)

def update_data(tickers, interval):
    # Adjust the update period for hourly data
    update_period_mapping = {
        '1d': '7d',
        '1wk': '7d',
        '1mo': '7d',
        '1h': '1d'  # Use one day for updating hourly data
    }
    directory_mapping = {
        '1d': 'DAILY',
        '1wk': 'WEEKLY',
        '1mo': 'MONTHLY',
        '1h': 'HOURLY'  # New entry for hourly data
    }
    data_dir = directory_mapping[interval]

    for ticker in tickers:
        filename = os.path.join(data_dir, f"{ticker}.csv")
        if os.path.exists(filename):
            print(f"Updating {interval} data for {ticker}")
            period = update_period_mapping[interval]
            data = yf.download(ticker, period=period, interval=interval)
            # Ensure no duplicate headers on update
            data.to_csv(filename, mode='a', header=False)
            print(f"Updated {interval} data for {ticker}")
        else:
            print(f"No existing file for {ticker} in {data_dir}. Please download initial data first.")
        time.sleep(1)

def user_selection():
    # Include hourly in the interval selection
    interval = input("Select data interval (daily, weekly, monthly, hourly): ")
    action = input("Choose action (initial or update): ")
    return interval, action

def main():
    tickers_df = pd.read_csv('SP500.csv', header=None)
    tickers = tickers_df[0].tolist()

    interval_input, action = user_selection()
    # Mapping now includes hourly
    interval_mapping = {'daily': '1d', 'weekly': '1wk', 'monthly': '1mo', 'hourly': '1h'}
    interval = interval_mapping.get(interval_input.lower())

    if not interval:
        print("Invalid interval selection. Please choose daily, weekly, monthly, or hourly.")
        return

    if action.lower() == 'initial':
        download_data(tickers, interval)
    elif action.lower() == 'update':
        update_data(tickers, interval)
    else:
        print("Invalid action selected. Please choose 'initial' or 'update'.")
        return

if __name__ == "__main__":
    main()
