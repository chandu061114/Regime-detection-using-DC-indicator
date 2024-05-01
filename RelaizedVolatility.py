import numpy as np
import pandas as pd

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

# Example usage:
# Assuming 'df' is your DataFrame with close prices
# df = add_realized_volatility_column(df)
