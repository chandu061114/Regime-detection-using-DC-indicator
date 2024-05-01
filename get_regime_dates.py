def get_regime_dates(dates, regimes):
    """
    Get the start and end dates for each regime.

    Parameters:
    dates (pd.DatetimeIndex): The dates corresponding to the indicator data.
    regimes (np.array): Array of detected states for the indicator.

    Returns:
    List of tuples: Each tuple contains the start and end dates for a regime.
    """
    regime_dates = []
    current_regime = regimes[0]
    start_date = dates[0]

    for i in range(1, len(regimes)):
        if regimes[i] != current_regime:
            end_date = dates[i - 1]
            regime_dates.append((current_regime, start_date, end_date))
            current_regime = regimes[i]
            start_date = dates[i]

    # Add the last regime
    regime_dates.append((current_regime, start_date, dates[-1]))

    return regime_dates
