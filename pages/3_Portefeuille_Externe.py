import pandas as pd
import streamlit as st
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
import matplotlib.pyplot as plt
import copy 
from datetime import datetime, timedelta
import requests
from utils import *
from finance_functions import *


key = "d8eabf9ca1dec61aceefd4b4a9b93992"
common_elements_investmentora()
page_header("Example des mandats GPD")

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
    portfolio_returns['PortfolioReturns'] = (returns * norm_alloc).sum(axis=1) 
    return portfolio_returns

start_date = st.sidebar.date_input("Date de Debut: ")
end_date = st.sidebar.date_input("Date de fin: ")
#key = st.sidebar.text_input("API KEY: ")

df = pd.DataFrame(columns=['Ticker', 'Allocation'],index=np.arange(2))

edited_df = st.experimental_data_editor(df)
tickers = edited_df['Ticker'].tolist()

portfolio_prices = get_monthly_stock_portfolio_prices(tickers, key)
print(portfolio_prices)
portfolio_returns = calculate_returns(portfolio_prices)

allocations = allocation_df(edited_df, portfolio_returns)
df = calculate_portfolio_returns(allocations, portfolio_returns)


#st.line_chart(df['PortfolioReturns'])

