from hmmlearn import hmm

def train_hmm_and_detect_regimes(indicator_series):
    """
    Train a Hidden Markov Model (HMM) on the indicator series and detect regimes.
    
    Parameters:
    indicator_series (pd.Series): Pandas Series of the indicator data.
    
    Returns:
    Tuple[np.array, pd.DatetimeIndex]: The hidden states detected by the HMM, and the corresponding dates.
    """
    # Drop NaN values from the series
    indicator_series_clean = indicator_series.dropna()

    if indicator_series_clean.empty:
        raise ValueError("The indicator series is empty after dropping NaN values.")

    # Reshape data for the HMM
    indicator_data = indicator_series_clean.values.reshape(-1, 1)
    
    # Initialize Gaussian HMM; here we assume 2 hidden states for 2 regimes
    model = hmm.GaussianHMM(n_components=2, covariance_type="diag", n_iter=10000)
    
    # Fit the HMM model
    model.fit(indicator_data)
    
    # Predict the hidden states (regimes)
    hidden_states = model.predict(indicator_data)
    
    return hidden_states, indicator_series_clean.index
