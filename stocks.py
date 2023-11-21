import numpy as np
import matplotlib.pyplot as plt


# global variables 
NUMBEROFDAYS = 100

INITIALPRICE = 100  # Initial stock price
DRIFT = 0.0001       # Drift term
VOLATILITY = 0.01    # Volatility term
NUMBEROFSIMULATIONS = 5  # Number of simulations

DT = 1/24


def generate_stock_prices(initial_price, drift, volatility, num_days, dt=1):
    prices = [initial_price]
    for _ in range(num_days - 1):
        daily_return = ( drift - volatility**2 / 2 ) * dt + volatility * np.random.normal(0, np.sqrt(dt))
        price_today = prices[-1] * np.exp(daily_return)
        prices.append(price_today)
    return prices



def generate_stock_prices(initialPrice, drift, volatility, numDays, dT):
    '''
    dT will be given in fraction of day -> updating every hour 
    '''

    lengthStock = int( 1/dT * numDays ) 


    stockEvolution = np.zeros(lengthStock)

    stockEvolution[0] = initialPrice

    # prices = [initial_price]
    for i in range(1, lengthStock):
        tempValue = drift * dT + volatility * np.random.normal(0, np.sqrt(dT))
        tempPrice = stockEvolution[i-1] * np.exp(tempValue)
        stockEvolution[i] = tempPrice
    return stockEvolution



# Generate stock prices
# plt.figure(figsize=(10, 6))
# for i in range(NUMBEROFSIMULATIONS):
#     prices = generate_stock_prices(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS)
#     plt.plot(prices, label = 'Stock No. ' + str(i))

stock = generate_stock_prices(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)
plt.plot(stock, label = 'Stock')





def CalculateMovingAverage(stock, dayNo, dT, daysConsidered, onlyClosingPrices): 

    if dayNo < daysConsidered: 
        return None

    numDays = len(stock) * dT

    stepsPerDay = int(len(stock) / numDays)

    # average over closing prices 
    partOfArray = stock[int( (dayNo - daysConsidered) * stepsPerDay) : int(dayNo * stepsPerDay)]

    # calculate average over every stepsperday-th element 
    if onlyClosingPrices: 
        avg = np.mean(partOfArray[:: stepsPerDay ])
    else: 

        # just take into account the whole array for the last few days 
        avg = np.mean(partOfArray)

    return avg



def CalculateZScore(stock, dayNo, dT, daysConsidered): 
    '''
    Z score over 1.5 indicates overvalued -> sell
    Z score under -1.5 indicates undervalued -> buy 
    '''

    if dayNo < daysConsidered: 
        return None

    mean = CalculateMovingAverage(stock, dayNo, dT, daysConsidered, False)

    numDays = len(stock) * dT

    stepsPerDay = int(len(stock) / numDays)

    partOfArray = stock[int( (dayNo - daysConsidered) * stepsPerDay) : int(dayNo * stepsPerDay)]

    print('tsetsetets', partOfArray)

    deviation = partOfArray[-1] - mean 

    std = np.std(partOfArray)

    print('testestsetetset', std)

    zScore = deviation / std

    return zScore










DAYSCONSIDERED = 5


averageList = []
zScoreList = []
daysList = np.arange(NUMBEROFDAYS) * 1/DT

for i in range(NUMBEROFDAYS):

    zScoreList.append(CalculateZScore(stock, i, DT, DAYSCONSIDERED))
    averageList.append(CalculateMovingAverage(stock, i, DT, DAYSCONSIDERED, True))


plt.plot(daysList, averageList, label = 'Moving Average, ' + str(DAYSCONSIDERED))

print(type(averageList), type(zScoreList))


plt.plot(daysList, zScoreList, label = 'Z-Score')
plt.title('Stock Price Simulation, Moving Average')
plt.xlabel('Hours')
plt.ylabel('Stock Price')
plt.legend()
# plt.show()


plt.show()