import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
pd.set_option('display.max_columns', 500)

#Basic Calculations

def allocation_df(allocations, portfolio_returns):
    allocation_df = pd.DataFrame(columns=portfolio_returns.columns, index=portfolio_returns.index)
    allocations = allocations.set_index("Ticker")
    allocations = allocations.astype(float)/100
    for ticker in allocation_df.columns:
        allocation_df[ticker] = allocations.loc[ticker, "Allocation"]

    return allocation_df

def calculate_portfolio_returns(allocations, returns):
    """
    Calculates the returns of a portfolio based on allocations. 
    Renormalizes the allocations if there are missing values in the returns dataframe
    
    Args:
        allocations (dataframe): allocations of portfolio
        returns (dataframe): returns of portfolio

    Returns:
        _type_: _description_
    """
    
    # Replace allocation values with NaN if there is a NaN in the corresponding returns column
    mask = returns.isna()
    allocations[mask] = np.nan    

    # Recalculate the allocations for each row
    row_sum = allocations.apply(lambda row: row.sum(skipna=True), axis=1)
    norm_alloc = allocations.div(row_sum, axis=0)
    portfolio_returns = (returns * norm_alloc).sum(axis=1) 
    return portfolio_returns

def get_daily_stock_portfolio_prices(portfolio, key):
    # Define the start and end dates (10 years ago from today)
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=3653)).strftime('%Y-%m-%d')

    dfs = []
    for stock in portfolio:
        dum = get_daily_stock_prices(stock, key)
        dum = dum[['date', 'close']]
        dum.columns = ['date', stock]
        dum.set_index('date', inplace=True)
        dfs.append(dum)

    merged_df = pd.concat(dfs, axis=1)


    merged_df.to_csv("tester_data.csv")
    return merged_df

def get_monthly_stock_portfolio_prices(portfolio, key):
    # Define the start and end dates (10 years ago from today)
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=3653)).strftime('%Y-%m-%d')

    dfs = []
    for stock in portfolio:
        dum = get_monthly_stock_prices(stock, key)
        dum = dum[['date', 'close']]
        dum.columns = ['date', stock]
        dum.set_index('date', inplace=True)
        dfs.append(dum)

    merged_df = pd.concat(dfs, axis=1)


    merged_df.to_csv("tester_data.csv")
    return merged_df



def calculate_returns(df):
    """
    Calculates the daily returns of each stock in a merged dataframe of historical prices.
    
    Args:
    df (pandas.DataFrame): A merged dataframe of historical prices for multiple stocks.
    
    Returns:
    pandas.DataFrame: A dataframe of daily returns for each stock in the input dataframe.
    """
    # Calculate the daily returns for each stock
    try:
        df = df.set_index("date")
    except:
        df = df

    returns_df = df.iloc[:, :].pct_change(-1)
    
    # Replace the first row of NaNs with 0s
    #returns_df.iloc[0, :] = 0

    returns_df.dropna(inplace=True)
    
    return returns_df

##### Financial Modelling Prep Functions
def get_monthly_stock_prices(stock, key):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=3653)).strftime('%Y-%m-%d')

    """
    gets stock prices on a monthly basis from FMP

    Args:
        stock (str): Ticker
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        _type_: _description_
    """
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?from={start_date}&to={end_date}&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['historical'])
    df["date"] = pd.to_datetime(df["date"])
    # Group by year and month, then select the maximum date within each group
    # Resample the dataframe to get the last day of each month
    # Set the "date" column as the index
    df.set_index("date", inplace=True)
    df_last_day = df.resample("M").last()

    # Reset the index
    df_last_day = df_last_day.reset_index()
    df_last_day = df_last_day[::-1]
    return df_last_day


def get_daily_stock_prices(stock, key):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=3653)).strftime('%Y-%m-%d')

    """gets stock prices on a daily basis from FMP

    Args:
        stock (str): Ticker
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        _type_: _description_
    """
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?from={start_date}&to={end_date}&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['historical'])
    return df

def key_metrics(stock, key):
    """gets stock key metrics like PE and roe

    Args:
        stock (str): Ticker
    Returns:
        _type_: _description_
    """
    url = f'https://financialmodelingprep.com/api/v3/key-metrics/{stock}?period=annual&limit=130&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df = df[['date', 'period', 'revenuePerShare', 'netIncomePerShare',
       'operatingCashFlowPerShare', 'freeCashFlowPerShare', 'cashPerShare',
       'bookValuePerShare', 'peRatio', 'priceToSalesRatio', 
       'pfcfRatio', 'freeCashFlowYield', 'debtToEquity', 'debtToAssets']]
    
    df[['revenuePerShare', 'netIncomePerShare',
       'operatingCashFlowPerShare', 'freeCashFlowPerShare', 'cashPerShare',
       'bookValuePerShare', 'peRatio', 'priceToSalesRatio', 
       'pfcfRatio', 'freeCashFlowYield', 'debtToEquity', 'debtToAssets']] = df[['revenuePerShare', 'netIncomePerShare',
       'operatingCashFlowPerShare', 'freeCashFlowPerShare', 'cashPerShare',
       'bookValuePerShare', 'peRatio', 'priceToSalesRatio', 
       'pfcfRatio', 'freeCashFlowYield', 'debtToEquity', 'debtToAssets']].round(2)
    
    df.rename(columns={'date':'Date', 'period':'Period', 'revenuePerShare':"Revenue Per Share", 'netIncomePerShare':"Net Income Per Share",
       'operatingCashFlowPerShare':"Operating Cash Flow Per Share", 'freeCashFlowPerShare': "FCF Per Share", 'cashPerShare':"Cash Per Share",
       'bookValuePerShare': "Book Value Per Share", 'peRatio': "P/E Ratio", 'priceToSalesRatio': "P/S Ratio", 
       'pfcfRatio': "P/FCF Ratio", 'freeCashFlowYield': "FCF Yield", 'debtToEquity': "Debt-to-Equity", 'debtToAssets': "Debt-to-Assets"}, inplace=True)
    df = df.loc[0,]
    df.T
    return df

def key_metrics_ttm(stock, key):
    """gets stock key metrics like PE and roe

    Args:
        stock (str): Ticker
    Returns:
        _type_: _description_
    """
    url = f'https://financialmodelingprep.com/api/v3/key-metrics-ttm/{stock}?period=annual&limit=130&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df = df[['revenuePerShareTTM', 'netIncomePerShareTTM',
       'operatingCashFlowPerShareTTM', 'freeCashFlowPerShareTTM', 'cashPerShareTTM',
       'bookValuePerShareTTM', 'peRatioTTM', 'priceToSalesRatioTTM', 
       'pfcfRatioTTM', 'freeCashFlowYieldTTM', 'debtToEquityTTM', 'debtToAssetsTTM']]
    
    df[['revenuePerShareTTM', 'netIncomePerShareTTM',
       'operatingCashFlowPerShareTTM', 'freeCashFlowPerShareTTM', 'cashPerShareTTM',
       'bookValuePerShareTTM', 'peRatioTTM', 'priceToSalesRatioTTM', 
       'pfcfRatioTTM', 'freeCashFlowYieldTTM', 'debtToEquityTTM', 'debtToAssetsTTM']] = df[['revenuePerShareTTM', 'netIncomePerShareTTM',
       'operatingCashFlowPerShareTTM', 'freeCashFlowPerShareTTM', 'cashPerShareTTM',
       'bookValuePerShareTTM', 'peRatioTTM', 'priceToSalesRatioTTM', 
       'pfcfRatioTTM', 'freeCashFlowYieldTTM', 'debtToEquityTTM', 'debtToAssetsTTM']].round(2)
    
    df.rename(columns={'revenuePerShareTTM':"Revenue Per Share", 'netIncomePerShareTTM':"Net Income Per Share",
       'operatingCashFlowPerShareTTM':"Operating Cash Flow Per Share", 'freeCashFlowPerShareTTM': "FCF Per Share", 'cashPerShareTTM':"Cash Per Share",
       'bookValuePerShareTTM': "Book Value Per Share", 'peRatioTTM': "P/E Ratio", 'priceToSalesRatioTTM': "P/S Ratio", 
       'pfcfRatioTTM': "P/FCF Ratio", 'freeCashFlowYieldTTM': "FCF Yield", 'debtToEquityTTM': "Debt-to-Equity", 'debtToAssetsTTM': "Debt-to-Assets"}, inplace=True)
    df = df.loc[0,]
    df.T
    return df


def company_profile(stock, key):
    """gets company profile

    Args:
        stock (str): Ticker

    Returns:
        _type_: _description_
    """
    url = f'https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df = df[['companyName', 'symbol', 'price', 'mktCap', 'exchangeShortName', 'sector', 'industry', 'ceo']]
    df.rename(columns={'companyName': 'Company Name', 'symbol':'Symbol', 'price':'Price', 'mktCap':"Market Cap", 'exchangeShortName':"Exchange Name", 'sector':'Sector', 'industry':'Industry', 'ceo':'CEO'}, inplace=True)
    df = df.T
    return df

def key_executives(stock, key):
    """gets key executives

    Args:
        stock (str): Ticker

    Returns:
        _type_: _description_
    """
    url = f'https://financialmodelingprep.com/api/v3/key-executives/{stock}?apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def format_percentage(numb):
    percentage = numb * 100
    formatted_percentage = "{:.2f}%".format(percentage)
    return formatted_percentage

##### Financial Modelling Prep Functions
def get_news_general(key):
    """gets stock news on a daily basis from FMP

    Args:
        stock (str): Ticker
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        _type_: _description_
    """
    url = f'https://financialmodelingprep.com/api/v4/general_news?page=0&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def get_news_stocks(key):
    """gets stock news on a daily basis from FMP

    Args:
        stock (str): Ticker
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        _type_: _description_
    """
    
    url = f'https://financialmodelingprep.com/api/v3/stock_news?limit=100&&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def get_news_stocks_specific(ticker, key):
    """gets stock news on a daily basis from FMP

    Args:
        stock (str): Ticker
        start_date (datetime): start date
        end_date (datetime): end date

    Returns:
        _type_: _description_
    """
    ""
    url = f'https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit=50&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

#earnings calls
def get_earnings_calls(ticker,quarter,year ,key):

    url = f'https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?quarter={quarter}&year={year}&apikey={key}'
    response = requests.get(url)
    data = response.json()[0]
    df = pd.DataFrame(data)
    return df

#financial
def get_quarterly_income_statement(ticker, key):
    "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=d8eabf9ca1dec61aceefd4b4a9b93992"
    url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=quarter&limit=8&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
 
    # Identify integer columns
    integer_columns = df.select_dtypes(include='integer').columns
    # Convert integer columns to floats
    df[integer_columns] = df[integer_columns].astype(float)
 
    #df = df.T
    #df.columns = df.loc['date']
    return df

def get_annual_income_statement(ticker, key):
    url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=10&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data).T
    df.columns = df.loc['date']
    return df

def get_quarterly_balance_statement(ticker, key):
    "https://financialmodelingprep.com/api/v3/balance-sheet-statement/AAPL?period=quarter&limit=400&apikey=d8eabf9ca1dec61aceefd4b4a9b93992"
    url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period=quarter&limit=8&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data).T
    df.columns = df.loc['date']
    return df

def get_annual_balance_statement(ticker, key):
    "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=d8eabf9ca1dec61aceefd4b4a9b93992"
    url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=8&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data).T
    df.columns = df.loc['date']
    return df

def get_quarterly_cashflow_statement(ticker, key):
    "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=d8eabf9ca1dec61aceefd4b4a9b93992"
    url = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period=quarter&limit=8&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data).T
    df.columns = df.loc['date']
    return df

def get_annual_cashflow_statement(ticker, key):
    "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=d8eabf9ca1dec61aceefd4b4a9b93992"
    url = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=8&apikey={key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data).T
    df.columns = df.loc['date']
    return df


key = "d8eabf9ca1dec61aceefd4b4a9b93992"

