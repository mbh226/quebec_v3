import yfinance as yf
from datetime import datetime, timedelta
import json
import pandas as pd

def fetch_portfolio_sharpe_ratio(portfolio, risk_free_rate=0.03):
    """
    Fetches the Sharpe Ratio for the entire portfolio based on historical prices.

    Parameters:
        portfolio: The portfolio data loaded from JSON.
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

        total_investment = sum(stock['amount_in_dollars'] for stock in portfolio['stocks'])

        # Loop through each stock in the portfolio
        for stock in portfolio['stocks']:
            ticker = stock['ticker']
            investment_amount = stock['amount_in_dollars']
            weight = investment_amount / total_investment  # Weight of the stock in the portfolio

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
                return None

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


def get_historical_stock_price(ticker, purchase_date):
    """
    Fetches the closing stock price on the specified purchase date.

    Parameters:
        ticker (str): The stock ticker symbol.
        purchase_date (str): The date of purchase in 'YYYY-MM-DD' format.

    Returns:
        float: The closing price on the purchase date, or None if no data is available.
    """
    stock = yf.Ticker(ticker)
    purchase_date_dt = datetime.strptime(purchase_date, '%Y-%m-%d')

    hist = stock.history(start=purchase_date_dt,
                         end=purchase_date_dt + timedelta(days=1), interval="1d")

    if not hist.empty:
        price_at_purchase = hist['Close'].iloc[0]
    else:
        price_at_purchase = None

    return price_at_purchase


def get_current_stock_price(ticker):
    """
    Fetches the latest available closing stock price.

    Parameters:
        ticker (str): The stock ticker symbol.

    Returns:
        float: The most recent closing price of the stock.
    """
    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d")['Close'].iloc[-1]
    return current_price


def calculate_investment_value(ticker, purchase_date, investment_amount):
    """
    Calculates the current value of an investment based on the historical stock price.

    Parameters:
        ticker (str): The stock ticker symbol.
        purchase_date (str): The date of purchase in 'YYYY-MM-DD' format.
        investment_amount (float): The amount of money initially invested.

    Returns:
        float or str: The current value of the investment, or an error message if no historical data is available.
    """
    initial_price = get_historical_stock_price(ticker, purchase_date)

    if initial_price == None:
        return "Invalid date or ticker"

    current_price = get_current_stock_price(ticker)

    shares_bought = investment_amount / initial_price
    current_value = shares_bought * current_price

    return current_value


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


def calculate_total_portfolio_value(portfolio):
    """
    Calculates the total current value of all stocks in the portfolio.

    Parameters:
        portfolio (dict): A dictionary containing the portfolio data.

    Returns:
        float: The total value of the portfolio.
    """
    total_value = 0
    for stock in portfolio['stocks']:
        ticker = stock['ticker']
        purchase_date = stock['date']
        investment_amount = stock['amount_in_dollars']

        current_value = calculate_investment_value(
            ticker, purchase_date, investment_amount)

        if isinstance(current_value, str):
            print(f"Error calculating value for {ticker}: {current_value}")
        else:
            total_value += current_value

    return total_value


# Load the portfolio JSON
portfolio_file = 'portfolio.json'
portfolio_data = load_portfolio(portfolio_file)

# Calculate total portfolio value
total_portfolio_value = calculate_total_portfolio_value(portfolio_data)
print("Total value of the portfolio is: $" + str(total_portfolio_value))
# Calculate sharpe ratio
#sharpe_ratio = fetch_portfolio_sharpe_ratio(portfolio_data)
#print("Sharpe ratio of the portfolio is " + str(sharpe_ratio))

stock_file = 'stock.json'
stock_data = load_portfolio(stock_file)
sharpe_ratio_stock = fetch_portfolio_sharpe_ratio(stock_data)
print("Sharpe ratio of the portfolio is " + str(sharpe_ratio_stock))
