import yfinance as yf
from datetime import datetime, timedelta, date
import json
import pandas as pd

def fetch_portfolio_sharpe_ratio(portfolio, risk_free_rate=0.03):
    """
    Fetches the Sharpe Ratio for the entire portfolio based on historical prices.

    Parameters:
        portfolio: A list of stock dictionaries with 'ticker' and 'nShares'.
        risk_free_rate (float): The risk-free rate for calculating the Sharpe Ratio (default is 3% annually).

    Returns:
        float: The Sharpe Ratio for the entire portfolio.
    """
    try:
        # Get today's date and one year ago's date
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

        # Create an empty DataFrame to hold daily portfolio returns
        portfolio_daily_returns = pd.DataFrame()

        # Calculate the total investment based on current prices and the number of shares
        total_investment = 0
        for stock in portfolio:
            ticker = stock['ticker']
            nShares = stock['nShares']

            # Fetch the current price of the stock
            try:
                current_price_data = yf.download(ticker, period='1d', progress=False)
                current_price = current_price_data['Close'].iloc[-1]
                total_investment += current_price * nShares
            except Exception as e:
                print(f"Error fetching current price for {ticker}: {e}")
                continue

        # Loop through each stock in the portfolio
        for stock in portfolio:
            ticker = stock['ticker']
            nShares = stock['nShares']

            # Calculate weight using today's price
            try:
                current_price_data = yf.download(ticker, period='1d', progress=False)
                current_price = current_price_data['Close'].iloc[-1]
                weight = (current_price * nShares) / total_investment  # Weight of the stock in the portfolio
            except Exception as e:
                print(f"Error fetching current price for {ticker}: {e}")
                continue

            # Use yfinance to get the historical prices for the past year
            stock_data = yf.Ticker(ticker)
            price_data = stock_data.history(start=start_date, end=end_date, interval="1d")

            # Check if data is available
            if not price_data.empty:
                # Get the closing prices and calculate daily returns
                closing_prices = price_data['Close']
                daily_returns = closing_prices.pct_change().dropna()

                # Add the weighted daily returns of the stock to the portfolio's daily returns
                portfolio_daily_returns[ticker] = daily_returns * weight
            else:
                print(f"No historical data available for {ticker}")
                continue

        # Sum the weighted returns to get the total portfolio daily returns
        portfolio_daily_returns['Portfolio'] = portfolio_daily_returns.sum(axis=1)

        # Calculate the average daily return and standard deviation of portfolio returns
        average_daily_return = portfolio_daily_returns['Portfolio'].mean()
        stddev_daily_return = portfolio_daily_returns['Portfolio'].std()

        # Assuming a risk-free rate of 3% per year (converted to daily rate)
        daily_risk_free_rate = risk_free_rate / 252  # 252 trading days in a year

        # Calculate the Sharpe Ratio for the portfolio
        sharpe_ratio = (average_daily_return - daily_risk_free_rate) / stddev_daily_return

        return sharpe_ratio

    except Exception as e:
        print(f"Error fetching historical prices for portfolio: {e}")
        return None

def load_portfolio(filename):
    """
    Loads the portfolio from a JSON file.

    Parameters:
        filename (str): The file path of the portfolio JSON.

    Returns:
        dict: The loaded portfolio data.
    """
    with open(filename, 'r') as f:
        portfolio = json.load(f)
    return portfolio


def fetch_stock_price(ticker, Date):
    """
    Fetch the Close value of the stock on the specific day.

    Parameters:
        ticker (str): Stock ticker symbol.
        Date (str): A date in 'YYYY-MM-DD' format.

    Returns:
        float: the Close value of the stock.
    """
    
    Date = datetime.fromisoformat(Date)

    # If date is in future
    if (Date.date() > date.today()):
        print('Future data no available')
        return None

    while True:
        stock_data = yf.download(ticker, start=Date, end=Date + timedelta(days=1), interval='1d', progress=False)
        if not stock_data.empty:
            stock_price = stock_data['Close'].iloc[0]
            break
        else:
            Date -= timedelta(days=1)

    return stock_price


def calculate_total_portfolio_value(portfolio, Date=datetime.today().strftime('%Y-%m-%d')):
    """
    Calculates the total current value of all stocks in the portfolio on the specific day.

    Parameters:
        portfolio (dict): A dictionary containing the portfolio data.
        Date (str): A date in 'YYYY-MM-DD' format. 

    Returns:
        float: The total value of the portfolio.
    """
    total_value = 0
    for stock in portfolio:
        ticker = stock['ticker']
        nShares = stock['nShares']
        stock_price = fetch_stock_price(ticker, Date)
        if stock_price:
            total_value += nShares * stock_price
        else:
            print('Error fetching prices for ' + ticker + ' on ' + Date)
            return None

    return total_value


# Load the portfolio JSON
portfolio_file = 'portfolio.json'
portfolio_data = load_portfolio(portfolio_file)

# Test
# Calculate total portfolio value on today
total_portfolio_value = calculate_total_portfolio_value(portfolio_data)
print("Total value of the portfolio today is: $" + str(total_portfolio_value))

# # Calculate total portfolio value on 2024-10-24
# total_portfolio_value = calculate_total_portfolio_value(portfolio_data, '2024-05-01')
# print("Total value of the portfolio on is 2024-05-01(Past) : $" + str(total_portfolio_value))

# # Calculate total portfolio value on 2024-01-01
# total_portfolio_value = calculate_total_portfolio_value(portfolio_data, '2024-01-01')
# print("Total value of the portfolio on is 2024-01-01(Holiday) : $" + str(total_portfolio_value))

# # Calculate total portfolio value on 2024-10-27
# total_portfolio_value = calculate_total_portfolio_value(portfolio_data, '2024-10-27')
# print("Total value of the portfolio on is 2024-10-27(Weekend) : $" + str(total_portfolio_value))

# # Calculate total portfolio value on 2025-10-27
# total_portfolio_value = calculate_total_portfolio_value(portfolio_data, '2025-10-27')
# print("Total value of the portfolio on is 2025-10-27(Future) : $" + str(total_portfolio_value))

# Calculate sharpe ratio
sharpe_ratio = fetch_portfolio_sharpe_ratio(portfolio_data)
print("Sharpe ratio of the portfolio is: " + str(sharpe_ratio))
