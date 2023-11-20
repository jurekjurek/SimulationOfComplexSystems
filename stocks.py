import numpy as np
import matplotlib.pyplot as plt

def generate_stock_prices(initial_price, drift, volatility, num_days, dt=1):
    prices = [initial_price]
    for _ in range(num_days - 1):
        daily_return = drift * dt + volatility * np.random.normal(0, np.sqrt(dt))
        price_today = prices[-1] * np.exp(daily_return)
        prices.append(price_today)
    return prices



def generate_stock_prices(initialPrice, drift, volatility, numDays, dT=1/24):
    '''
    dT will be given in fraction of day 
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

# Parameters
initial_price = 100  # Initial stock price
drift = 0.0001       # Drift term
volatility = 0.01    # Volatility term
num_days = 5       # Number of trading days in a year
num_simulations = 5  # Number of simulations

# Generate stock prices
plt.figure(figsize=(10, 6))
for i in range(num_simulations):
    prices = generate_stock_prices(initial_price, drift, volatility, num_days)
    plt.plot(prices, label = 'Stock No. ' + str(i))

plt.title('Stock Price Simulation using Geometric Brownian Motion')
plt.xlabel('Days')
plt.ylabel('Stock Price')
plt.legend()
plt.show()


'''
different trading strategies: 

Buy and Hold 

'''


def BuyAndHold(stockEvolution): 
    '''
    given a stock over a certain number of days 
    '''

    buyPrice = stockEvolution[0]
    sellPrice = stockEvolution[-1]

    return sellPrice - buyPrice


def MovingAverage(stockEvolution, daysConsidered, dT, sellFactor ): 
    '''
    this function takes into account the last n days of the stock market 
    '''

    avg = 0

    stepsPerDay = int( 1 / dT)

    lower = False
    buy = False

    # consider last few days
    for dayNo in range(daysConsidered): 

        # sum up closing prices over days 
        avg += stockEvolution[int( dayNo * int(1/dT) )]

    avg /= daysConsidered


    buyPrices = []
    sellPrices = []

    for i in range(len(stockEvolution)):

        # update Avg
        if i%stepsPerDay == 0: 

            dayNo = int( num_days / i )

            partOfArray = stockEvolution[i: (dayNo + daysConsidered) * stepsPerDay]

            avg = np.mean(stockEvolution[:: stepsPerDay ].reshape(-1, stepsPerDay), axis=1)


        if stockEvolution[i] < avg: 
            lower = True
        
        if stockEvolution[i] >= avg and lower == True: 
            buyPrice = stockEvolution[i]
            buy = True
            lower = False 
            buyPrices.append(buyPrice)

        if buy == True and stockEvolution[i] < avg * sellFactor: 
            buy = False 
            lower = True
            sellPrice = stockEvolution[i]
            sellPrices.append(sellPrice)


        # if last element -> sell 

        if i == len(stockEvolution): 
            sellPrice = stockEvolution[i]
            sellPrices.append(sellPrice)

    return buyPrices, sellPrices 


def OtherMovingAverage(): 
    '''
    Use short term and long term average and buy if they cross 
    '''
    return None 


def MeanReversion(): 
    '''
    No, consider two Stocks of the same category. If one falls, and the other does not, this might be an opportunity to buy 
    '''
    return None



def IntraDayMeanReversion(): 
    return None 


def MomentumStrategy(): 
    '''
    Buy when 2nd derivative == 0
    '''


def BuyMorningSellNight(): 
    '''
    Easy strategy where we buy every morning and sell every night 
    '''
    return None 



def BuyAndSellRandomly(): 
    '''
    Buy at random times and sell at random times. 
    '''
    return None 


def Scalping(timeA, timeB): 
    '''
    stock has been rising for a certain short time (timeA)  -> buy 
    stock has been rising for a long time (timeB)           -> sell
    '''


def CompareStrategies(stockEvolution, taxFactor): 
    '''
    this function compares the different trading strategies to each other
    '''




