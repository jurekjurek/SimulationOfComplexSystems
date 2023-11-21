from stocks import * 










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

            # calculate average over every stepsperday-th element 
            avg = np.mean(partOfArray[:: stepsPerDay ].reshape(-1, stepsPerDay), axis=1)


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

    Calculate mean over certain timeframe, then calculate standard deviation and Z value indicating if a price is lower or higher than actual value


    '''
    return None



def RangeTrading():
    '''
    if the Stock is clearly  - only shortterm!!! - between a min and a max value for the last x timesteps -> buy when high in this range 
    sell when break out of range... (some indicators exist ... )
    '''

    return None 


def BreakOut(): 
    ''''
    Again, a range between min and max. 
    And here, if the stock breaks out above the max, buy and sell as soon as it falls again. 
    '''



def IntraDayMeanReversion(): 
    return None 


def MomentumStrategy(): 
    '''
    Buy when 2nd derivative == 0
    '''



def ReversalTrading(): 
    '''
    If it has been falling for a long time and now starts rising again -> buy 
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

