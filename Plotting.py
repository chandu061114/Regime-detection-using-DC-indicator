import matplotlib.pyplot as plt


def plot_regimes(dates, dc_states, rv_states):
    """
    Plot the regimes detected by the HMM for the DC indicator and the RV on the same plot.
    
    Parameters:
    dates (pd.DatetimeIndex): The dates corresponding to the indicator data.
    dc_states (np.array): Array of detected states for the DC indicator.
    rv_states (np.array): Array of detected states for the RV.
    """
    plt.figure(figsize=(14, 7))
    
    # Plot the DC indicator regimes
    plt.subplot(2, 1, 1)
    plt.title('Regimes Detected using DC Indicator')
    plt.plot(dates, dc_states, label='DC Indicator Regimes', drawstyle='steps-post')
    plt.legend()
    
    # Plot the RV regimes
    plt.subplot(2, 1, 2)
    plt.title('Regimes Detected using RV')
    plt.plot(dates, rv_states, label='RV Regimes', drawstyle='steps-post', color='orange')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
def plot_with_regime_background(data, indicator_column, regimes, title, ylabel, colors):
    """
    Plot the indicator values with regime backgrounds.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing dates and indicator data.
    indicator_column (str): Column name of the indicator in the DataFrame.
    regimes (np.array): Array of detected states for the indicator.
    title (str): The title for the plot.
    ylabel (str): Label for the y-axis.
    colors (dict): Dictionary mapping regimes to colors.
    """
    # Drop NaN values and align dates
    indicator_data = data[indicator_column].dropna()
    dates = indicator_data.index

    plt.figure(figsize=(10, 5))
    plt.title(title)

    # Ensure regimes array matches the length of non-NaN indicator data
    regimes = regimes[:len(indicator_data)]

    # Plot the background color based on regimes
    for i in range(regimes.min(), regimes.max() + 1):
        plt.fill_between(dates, indicator_data.min(), indicator_data.max(), 
                         where=(regimes == i), color=colors[i], alpha=0.5, step='post')

    # Plot the indicator values
    plt.plot(dates, indicator_data, label=ylabel, color='black', linewidth=2)
    plt.ylabel(ylabel)
    plt.xlabel('Date')
    plt.legend()
    plt.show()

