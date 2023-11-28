from stocks import * 
import random

def BuyAndHold(stock, timeStep): 
    '''
    given a stock over a certain number of days 

    Each of the trading strategy functions has two booleans: buy and sell
    buy indicates if it would be a good idea to buy, given the timestep as well as the stock 
    sell indicates if it would be a good idea to sell. 
    '''

    buy = False
    sell = False 

    if timeStep == 0: 

        # if first possible option to trade 
        buy = True 

    if timeStep == len(stock)-1: 

        # if last possible option to trade, sell 
        sell = True 
        

    return buy, sell 





# stock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)








def MovingAverage(stock, timeStep, dayRange, dT): 
    '''
    If we notice an upwards or downwards trend in the moving average, buy (sell).

    return: Two booleans, indicating if we want to sell or buy
    '''

    currentPrice = stock[timeStep]

    currentDay = int(timeStep * dT)

    # if we have not passed 3 days yet, return not buy, not sell
    if currentDay * 1/dT <= timeStep + (3*1/dT): 
        return False, False

    # if in the last 3 days, the average went only up, buy 
    avg1 = CalculateMovingAverage(stock, currentDay-2, dT, dayRange, True)
    avg2 = CalculateMovingAverage(stock, currentDay-1, dT, dayRange, True)
    avg3 = CalculateMovingAverage(stock, currentDay, dT, dayRange, True)

    if avg1 < avg2 and avg2 < avg3: 
        return True, False
    
    elif avg1 > avg2 and avg2 > avg3: 
        return False, True

    else: 
        return False, False




def ExponentialMovingAverage(stock, timeStep): 
    '''
    
    '''
    return None 

def CrossOverMovingAverage(stock, timeStep, dayRangeLong, dayRangeShort, dT): 
    '''
    Use short term and long term average and buy if they cross 

    We want to make use of short time fluctuations in the market using this strategy 

    '''
    currentPrice = stock[timeStep]

    currentDay = int(timeStep * 1/dT)


    avgLong1 = CalculateMovingAverage(stock, currentDay, dT, dayRangeLong, True)
    avgLong2 = CalculateMovingAverage(stock, currentDay-1, dT, dayRangeLong, True)

    avgShort1 = CalculateMovingAverage(stock, currentDay, dT, dayRangeShort, True)
    avgShort2 = CalculateMovingAverage(stock, currentDay-1, dT, dayRangeShort, True)

    # if shortrange crosses over longrange, buy 
    if avgShort1 < avgLong1 and avgShort2 > avgLong2: 
        return True, False 

    # if shortrange crosses under longrange, sell 
    elif avgShort1 > avgLong1 and avgShort2 < avgLong2: 
        return False, True 

    else: 
        return False, False
     



def MeanReversion(stock, timeStep, dT, dayRange): 
    '''
    -> use Z value 

    '''

    currentPrice = stock[timeStep]

    currentDay = int(timeStep * 1/dT)

    zValue = CalculateZScore(stock, currentDay, dT, dayRange)

    # buy, undervalued
    if zValue < -1.5: 
        return True, False 

    # sell, overvalued
    elif zValue > 1.5: 
        return False, True 

    # neither buy nor sell 
    else: 
        return False, False
        



def RangeTrading(stock, dayRange, dT, rangeLimit, offset, timeStep):
    '''
    if the Stock is clearly  - only shortterm!!! - between a min and a max value for the last x timesteps -> buy when high in this range 
    sell when break out of range... (some indicators exist ... )

    buy when at lower range max 
    sell when at higher range max 

    offset is distance from limit. If limit - offset is the current price, we buy. Else we do not. 

    '''

    currentPrice = stock[timeStep]

    if int(dayRange * 1/dT) > timeStep: 
        return False, False
            
    arrayOfInterest = stock[timeStep - int(dayRange * 1/dT): timeStep]

    # look at maximum of this part of the stock 
    upperLimit = np.max(arrayOfInterest)

    # find min in array (lower range limit)
    lowerLimit = np.min(arrayOfInterest)

    # if there exists a range within the margin we defined 
    if upperLimit - lowerLimit < rangeLimit: 

        # if currentprice is within offset away from upper limit -> sell 
        if currentPrice >= upperLimit * offset:
            return False, True 

        elif currentPrice <= lowerLimit * offset: 
            return True, False 

        else: 
            return False, False 




def BreakOut(stock, dayRange, dT, rangeLimit, offset, timeStep): 
    ''''
    Again, a range between min and max. 
    And here, if the stock breaks out above the max, buy and sell as soon as it falls again. 





    You have to check this again!!!!
    '''

    currentPrice = stock[timeStep]

    if int(dayRange * 1/dT) > timeStep: 
        return False, False
            
    # we want to break out of the range!! 
    arrayOfInterest = stock[timeStep - int((dayRange + 1) * 1/dT): timeStep - int((1) * 1/dT)]

    # look at maximum of this part of the stock 
    upperLimit = np.max(arrayOfInterest)

    # find min in array (lower range limit)
    lowerLimit = np.min(arrayOfInterest)

    # if there exists a range within the margin we defined 
    if upperLimit - lowerLimit < rangeLimit: 

        # if currentprice is within offset away from upper limit -> sell 
        if currentPrice > upperLimit:
            return False, True 

        elif currentPrice <= lowerLimit * offset: 
            return True, False 

        else: 
            return False, False 



# def IntraDayMeanReversion(stock, timeStep): 
#     return None 


# def MomentumStrategy(stock, timeStep): 
#     '''
#     Buy when 2nd derivative == 0
#     '''



def ReversalTrading(stock, timeStep, timeA, timeB): 
    '''
    If it has been falling for a long time and now starts rising again -> buy 

    Essentially the same as scalping somehow

    '''
    buy, sell = True

    for i in range(timeA): 
        # if stock has not been constantly increasing in the last timeA timesteps, we do not buy 
        if not stock[timeStep - i] > stock[timeStep - (i+1)]: 
            buy = False
        else: 
            continue
        
    for j in range(timeB): 
        # if stock has not been constantly decreasing in the last timeB timesteps, we do not sell
        if not stock[timeStep - j] < stock[timeStep - (j+1)]:
            sell = False

        else: 
            continue


    return buy, sell


def BuyMorningSellNight(stock, timeStep, dT): 
    '''
    Easy strategy where we buy every morning and sell every night 
    '''
    dayLength = len(stock) * dT 

    if timeStep % dayLength == 0: 
        return True, False
    if timeStep % (dayLength + 1) == 0: 
        return False, True


    return False, False  



def BuyAndSellRandomly(stock, timeStep, thresHoldProbability): 
    '''
    Buy at random times and sell at random times. 
    Independent of the timestep or anything else. 
    '''

    randomNumberBuy = random.random()
    randomNumberSell = random.random()

    if randomNumberBuy < thresHoldProbability: 
        return True, False

    if randomNumberSell < thresHoldProbability: 
        return False, True
    


    return False, False 


def Scalping(stock, timeStep, timeA, timeB): 
    '''
    stock has been rising for a certain short time (timeA)  -> buy 
    stock has been rising for a long time (timeB)           -> sell

    timeA and timeB are given in timeSteps
    '''

    buy, sell = True

    for i in range(timeA): 
        # if stock has not been constantly increasing in the last timeA timesteps, we do not buy 
        if not stock[timeStep - i] > stock[timeStep - (i+1)]: 
            buy = False
        else: 
            continue
        
    for j in range(timeB): 
        # if stock has not been constantly decreasing in the last timeB timesteps, we do not sell
        if not stock[timeStep - j] < stock[timeStep - (j+1)]:
            sell = False

        else: 
            continue


    return buy, sell


