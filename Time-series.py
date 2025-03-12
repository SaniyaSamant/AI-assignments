# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from pandas.plotting import autocorrelation_plot

# Load sample dataset
data = sm.datasets.co2.load_pandas().data
data = data['co2'].resample('M').mean().fillna(method='ffill')

# Descriptive statistics
mean = data.mean()
median = data.median()
std_dev = data.std()
variance = data.var()
range_ = data.max() - data.min()

# Print basic statistics
print(f"Mean: {mean}")
print(f"Median: {median}")
print(f"Standard Deviation: {std_dev}")
print(f"Variance: {variance}")
print(f"Range: {range_}")

# Decompose the time series
decomposition = seasonal_decompose(data, model='additive')
decomposition.plot()
plt.show()

# Augmented Dickey-Fuller test for stationarity
result = adfuller(data)
print(f"ADF Statistic: {result[0]}")
print(f"p-value: {result[1]}")

# Autocorrelation plot
autocorrelation_plot(data)
plt.show()

# Forecasting using ARIMA model
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(data, order=(1, 1, 1))
model_fit = model.fit()
forecast = model_fit.forecast(steps=12)
print(f"Forecast for next 12 months: {forecast}")

# Plotting the forecast
plt.plot(data, label='Original')
plt.plot(pd.Series(forecast, index=pd.date_range(data.index[-1], periods=12, freq='M')), label='Forecast', color='red')
plt.legend()
plt.show()
