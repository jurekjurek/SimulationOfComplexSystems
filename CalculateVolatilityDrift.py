import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stocks import *

# Load the data
data = pd.read_csv("real_prices.csv")
deltaT = 1 / 24

# Extract date of data 1
first_datetime = str(data['Datetime'][0]).split()
date = first_datetime[0]

# Define array to store close prices of days
day_close = []

for i in range(len(data)):
    # Extract date of data i
    iteration_datetime = str(data['Datetime'][i]).split()
    iteration_date = iteration_datetime[0]

    # judge if it is a new day
    if date != iteration_date:
        date = iteration_date

        # Add close price of yesterday
        day_close.append(data['Close'][i - 1])

# Add close price of the final day
day_close.append(data['Close'].iloc[-1])

# Calculate profit rate
profit_rates = np.zeros(len(day_close) - 1)

for i in range(len(profit_rates)):
    profit_rates[i] = day_close[i + 1] / day_close[i]

# Calculate log profit rate
log_profit_rates = np.log(profit_rates)

# Calculate drift
drift = np.mean(log_profit_rates)

# Calculate volatility
volatility = np.std(log_profit_rates)

stock_length = len(data['Close'])
initial_price = day_close[0]


# Generate simulated prices
simulated_prices = GenerateStocks(initial_price, drift, volatility, stock_length, deltaT)



# Plotting
plt.plot(data['Close'], label='Real Prices')
plt.plot(simulated_prices, label='Simulated Prices')
plt.legend()
plt.show()

# Save simulated prices to CSV
np.savetxt('simulated_prices.csv', simulated_prices, delimiter=',')
