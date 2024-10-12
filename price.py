import yfinance as yf
from datetime import datetime, timedelta


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
        return "No data available for the specified purchase date."

    current_price = get_current_stock_price(ticker)

    shares_bought = investment_amount / initial_price
    current_value = shares_bought * current_price

    return current_value


# Ex usage
ticker = input("Enter stock ticker (AAPL): ")
purchase_date = input("Enter the purchase date (YYYY-MM-DD): ")
investment_amount = float(input("Enter the investment amount: "))

current_value = calculate_investment_value(
    ticker, purchase_date, investment_amount)

print("Current value of the porfolio is: " + str(current_value))
