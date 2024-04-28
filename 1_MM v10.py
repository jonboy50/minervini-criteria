# Always manually check on tradingview
#- wll get the odd dropped criteria as this program works from weekly data
# Minervini Screener


import pandas as pd
import os

# Define the folder path where the historical data CSV files are located
data_folder_path = "datasets/SP500/WEEKLY/"

# Function to analyse a single stock ticker
def analyze_stock(stock_ticker):
    # Build the file path for the CSV containing historical data for the stock
    file_path = os.path.join(data_folder_path, f"{stock_ticker}.csv")

    # Read the historical data from the CSV file
    stock_data = pd.read_csv(file_path)
    if stock_data.empty or len(stock_data) < 40 or stock_data['Volume'].iloc[-1] == 0:
        return None

    stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Convert the 'Date' column to datetime format
    stock_data.set_index('Date', inplace=True)  # Set the 'Date' column as the DataFrame index

    # Perform the analysis for the current stock ticker (

    # Calculate the 30-week and 40-week moving average price lines
    stock_data['30WeekSMA'] = stock_data['Close'].rolling(window=30).mean()
    stock_data['40WeekSMA'] = stock_data['Close'].rolling(window=40).mean()

    # Check if the current stock price is above both moving average price lines (Criterion 1)
    stock_data['IsAbove30WeekAnd40WeekSMA'] = stock_data['Close'] > stock_data[['30WeekSMA', '40WeekSMA']].min(axis=1)

    # Check if the 30-week moving average is above the 40-week moving average (Criterion 2)
    stock_data['Is30WeekSMAAbove40WeekSMA'] = stock_data['30WeekSMA'] > stock_data['40WeekSMA']

    # Calculate the 10-week moving average
    stock_data['10WeekSMA'] = stock_data['Close'].rolling(window=10).mean()

    # Check if the 10-week moving average is greater than the 30-week moving average (Criterion 4)
    stock_data['Is10WeekSMAGreaterThan30WeekSMA'] = stock_data['10WeekSMA'] > stock_data['30WeekSMA']

    # Check if the 10-week moving average is greater than the 40-week moving average (Criterion 4a)
    stock_data['Is10WeekSMAGreaterThan40WeekSMA'] = stock_data['10WeekSMA'] > stock_data['40WeekSMA']

    # Calculate the 40-week moving average from 4 weeks ago
    stock_data['40WeekSMA_4WeeksAgo'] = stock_data['Close'].shift(4).rolling(window=40).mean()

    # Check if the 40-week moving average from 4 weeks ago is lower than today's 40-week MA (Criterion 3)
    stock_data['Is40WeekSMAFrom4WeeksAgoLower'] = stock_data['40WeekSMA_4WeeksAgo'] < stock_data['40WeekSMA']

    # Check if the last weekly bar's close price is greater than the 10-week moving average value (Criterion 5)
    stock_data['IsLastWeeklyCloseAbove10WeekSMA'] = stock_data['Close'].iloc[-1] > stock_data['10WeekSMA'].iloc[-1]

    # Calculate the 52-week low price
    stock_data['52WeekLow'] = stock_data['Close'].rolling(window=52).min()

    # Check if the current stock price is at least 25% above its 52-week low price (Criterion 6)
    stock_data['IsCurrentPriceAbove25Percent52WeekLow'] = stock_data['Close'].iloc[-1] >= 1.25 * stock_data['52WeekLow'].iloc[-1]

    # Calculate the 52-week high price
    stock_data['52WeekHigh'] = stock_data['Close'].rolling(window=52).max()

    # Check if the current stock price is within at least 25% of its 52-week high price (Criterion 7)
    stock_data['IsCurrentPriceWithin25Percent52WeekHigh'] = stock_data['Close'].iloc[-1] >= 0.75 * stock_data['52WeekHigh'].iloc[-1]

    # Check if the stock meets all the criteria
    meets_all_criteria = all(stock_data[criterion].iloc[-1] for criterion in [
        'IsAbove30WeekAnd40WeekSMA',
        'Is30WeekSMAAbove40WeekSMA',
        'Is40WeekSMAFrom4WeeksAgoLower',
        'Is10WeekSMAGreaterThan30WeekSMA',
        'Is10WeekSMAGreaterThan40WeekSMA',
        'IsLastWeeklyCloseAbove10WeekSMA',
        'IsCurrentPriceAbove25Percent52WeekLow',
        'IsCurrentPriceWithin25Percent52WeekHigh'
    ])

    # Return the stock ticker if it meets all the criteria
    if meets_all_criteria:
        return stock_ticker
    else:
        return None


def main():
    # Get a list of all CSV files in the data folder
    csv_files = [f for f in os.listdir(data_folder_path) if f.endswith('.csv')]

    # Extract the stock tickers from the file names (remove the '.csv' extension)
    stock_tickers = [f[:-4] for f in csv_files]

    # List to store the stock tickers that meet all the criteria
    selected_stock_tickers = []

    # Loop through each stock ticker and analyze the stock
    for stock_ticker in stock_tickers:
        selected_ticker = analyze_stock(stock_ticker)
        if selected_ticker:
            selected_stock_tickers.append(selected_ticker)

    # Output the list of stock tickers that meet all the criteria
    print("Stock tickers that meet all the criteria:")
    for ticker in selected_stock_tickers:
        print("LSE:",(ticker))


if __name__ == "__main__":
    main()
