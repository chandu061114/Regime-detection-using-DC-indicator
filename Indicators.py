import pandas as pd
import numpy as np
from hmmlearn import hmm


def directional_change_events(data, theta=0.2):

    # Copy the dataframe
    data = data.copy()

    # Create the necessary columns
    data["Event"] = 0.0
    data["pt"] = 0.0 # current price
    data["ph"] = 0.0 # highest price
    data["pl"] = 0.0 # lowest price
    data["ph_index"] = 0 # highest price index
    data["pl_index"] = 0 # lowest price index

    # Set the initial event variable value
    event = "upward" # initial event

    # Set the initial value for some columns
    data['Close'][0]
    data["pt"].iloc[0] = data['Close'].iloc[0] # current price
    data["ph"].iloc[0] = data['Close'].iloc[0] # highest price
    data["pl"].iloc[0] = data['Close'].iloc[0] # lowest price

    # Create loop to run through each date
    for t in range(0, len(data.index)):
        # Check if we're on a downward trend
        if event == "downward":
            # Check if the close price is less than the low price
            if data["Close"].iloc[t] < data["pl"].iloc[(t-1)]:
                # Set the low price as the close price
                data['pl'].iloc[t] = data["Close"].iloc[t]
                # Set the low price index as the current index
                data["pl_index"].iloc[t] = t
            # Check if the close price is higher than the low price by the theta threshold
            if data["Close"].iloc[t] >= data["pl"].iloc[(t-1)] * (1 + theta):
                # Set a low price variable as the previous low price index
                pl_index = data["pl_index"].iloc[(t-1)]
                # Trigger an upward trend event
                data['Event'].iloc[pl_index] = 1 
                # Set the event variable to upward
                event = "upward"
                # Set the high price as the close price                
                data["ph"].iloc[t] = data["Close"].iloc[t]
                # Set the high price index as the current index
                data["ph_index"].iloc[t] = t
        # Check if we're on a upward trend
        elif event == "upward":
            # Check if the close price is higher than the high price
            if data["Close"].iloc[t] > data["ph"].iloc[(t-1)]:
                # Set the high price as the close price
                data["ph"].iloc[t] = data["Close"].iloc[t]
                # Set the high price index as the current index
                data["ph_index"].iloc[t] = t
            # Check if the close price is less than the high price by the theta threshold
            if data["Close"].iloc[t] <= data["ph"].iloc[(t-1)] * (1 - theta):
                # Set a high price variable as the previous high price index
                ph_index = data["ph_index"].iloc[(t-1)]
                # Trigger a downward trend event
                data['Event'].iloc[ph_index] = -1 # start downturn event
                # Set the event variable to downward
                event = "downward"
                # Set the low price as the close price
                data["pl"].iloc[t] = data["Close"].iloc[t]
                # Set the low price index as the current index
                data["pl_index"].iloc[t] = t

    # Forward-fill the low and high price indexes
    data['ph_index'] = data['ph_index'].replace(to_replace=0, method='ffill')
    data['pl_index'] = data['pl_index'].replace(to_replace=0, method='ffill')

    # Forward-fill the low and high prices
    data['ph'] = data['ph'].replace(to_replace=0, method='ffill')
    data['pl'] = data['pl'].replace(to_replace=0, method='ffill')

    #data['Event'] = data['Event'].replace(to_replace=0, method='ffill')

    # Compute the TMV indicator and forward-fill it
    data['TMV'] = np.where(data['Event']==-1, abs(data['ph']-data['pl'])/(data['pl']*theta),0)
    data['TMV'] = np.where(data['Event']==1, abs(data['pl']-data['ph'])/(data['ph']*theta),data['TMV'])
    data['TMV'] = data['TMV'].replace(to_replace=0, method='ffill')

    # Compute the time-completion-for-a-trend indicator and forward-fill it
    data['T'] = np.where((data['Event']==-1) | (data['Event']==1), abs(data['ph_index']-data['pl_index']),0)
    data['T'] = data['T'].replace(to_replace=0, method='ffill')

    # Compute the time-adjusted-return indicator and forward-fill it
    data['R'] = np.where((data['Event']==-1) | (data['Event']==1), np.log(data['TMV']/data['T']*theta),0)
    #data['R'] = np.log(data['TMV']/data['T']*theta)
    data['R'] = data['R'].replace(to_replace=0, method='ffill')
    
    return data


def add_realized_volatility_column(data):
    """
    Calculate the Realized Volatility (RV) from close prices and add it as a column to the DataFrame.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing the close prices with a 'Close' column.
    
    Returns:
    pd.DataFrame: The input DataFrame with an added 'RV' column for realized volatility.
    """
    # Calculate log returns from the close prices
    log_returns = np.log(data['Close'] / data['Close'].shift(1))
    
    # Calculate the rolling sum of squared log returns
    # Here we'll use a rolling window to calculate RV for each point as a cumulative measure
    # You can define the window size as needed; here I assume a window size of 1 day for simplicity
    window_size = 1  # Change the window size as required for your analysis
    data['RV'] = log_returns.rolling(window=window_size).apply(lambda x: np.sqrt(np.sum(x**2)), raw=True)
    
    # Handle or drop NaN values
    data['RV'].fillna(0, inplace=True)
    
    return data

