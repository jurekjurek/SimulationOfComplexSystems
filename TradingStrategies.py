from stocks import * 
import random


# 1

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






# 2

def MovingAverage(stock, timeStep): 
    '''
    If we notice an upwards or downwards trend in the moving average, buy (sell).

    return: Two booleans, indicating if we want to sell or buy
    '''
    dayRange = 10
    dT = 1/24
    timeFrame = 3

    currentPrice = stock[timeStep]

    currentDay = int(timeStep * dT)

    # if we have not passed 3 days yet, return not buy, not sell
    # if timeStep <= (3*1/dT): 
    #     return False, False

    # if in the last 3 days, the average went only up, buy 
    avgDayList = []
    for i in range(timeFrame):
        avgDayList.append(CalculateMovingAverage(stock, currentDay-i, dT, dayRange, False))
        # avg2 = CalculateMovingAverage(stock, currentDay-1, dT, dayRange, True)
        # avg3 = CalculateMovingAverage(stock, currentDay, dT, dayRange, True)

    if None in avgDayList: 
        return False, False

    # if avg1 < avg2 and avg2 < avg3: 
    #     return True, False
    
    # elif avg1 > avg2 and avg2 > avg3: 
    #     return False, True

    # in descending order 
    if avgDayList == sorted(avgDayList, reverse=True):
        return True, False 
    
    # in ascending order
    elif avgDayList == sorted(avgDayList): 
        return False, True

    else: 
        return False, False





# 3

def CrossOverMovingAverage(stock, timeStep): 
    '''
    Use short term and long term average and buy if they cross 

    We want to make use of short time fluctuations in the market using this strategy 

    '''
    dayRangeLong = 20
    dayRangeShort = 5
    dT = 1/24



    currentDay = int(timeStep * dT)


    avgLong1 = CalculateMovingAverage(stock, currentDay, dT, dayRangeLong, True)
    avgLong2 = CalculateMovingAverage(stock, currentDay-1, dT, dayRangeLong, True)

    avgShort1 = CalculateMovingAverage(stock, currentDay, dT, dayRangeShort, True)
    avgShort2 = CalculateMovingAverage(stock, currentDay-1, dT, dayRangeShort, True)

    if avgLong1 == None or avgLong2 == None or avgShort1 == None or avgShort2 == None: 
        return False, False

    # if shortrange crosses over longrange, buy 
    if avgShort1 > avgLong1 and avgShort2 < avgLong2: 
        return True, False 

    # if shortrange crosses under longrange, sell 
    elif avgShort1 < avgLong1 and avgShort2 > avgLong2: 
        return False, True 

    else: 
        return False, False
     




# 4

def MeanReversion(stock, timeStep): 
    '''
    -> use Z value 

    '''
    dayRange = 10
    dT = 1/24

    currentPrice = stock[timeStep]

    currentDay = int(timeStep * dT)

    zValue = CalculateZScore(stock, currentDay, dT, dayRange)

    if zValue == None: 
        return False, False

    # buy, undervalued
    if zValue < -1.5: 
        return True, False 

    # sell, overvalued
    elif zValue > 1.5: 
        return False, True 

    # neither buy nor sell 
    else: 
        return False, False
        







# 5

def RangeTrading(stock, timeStep):
    '''
    if the Stock is clearly  - only shortterm!!! - between a min and a max value for the last x timesteps -> buy when high in this range 
    sell when break out of range... (some indicators exist ... )

    buy when at lower range max 
    sell when at higher range max 

    offset is distance from limit. If limit - offset is the current price, we buy. Else we do not. 

    '''
    dayRange = 10
    dT = 1/24
    rangeLimit = 10
    offset = 0.1 
    

    currentPrice = stock[timeStep]

    if int(dayRange * 1/dT) > timeStep: 
        return False, False
            
    # we want to include this timestep in the range as well 
    arrayOfInterest = stock[timeStep - int((dayRange-1) * 1/dT): timeStep+1]

    # look at maximum of this part of the stock 
    upperLimit = np.max(arrayOfInterest)

    # find min in array (lower range limit)
    lowerLimit = np.min(arrayOfInterest)

    # if, in this timestep not within range, return 
    if currentPrice > upperLimit or currentPrice < lowerLimit: 
        return False, False

    # if there exists a range within the margin we defined 
    if upperLimit - lowerLimit < rangeLimit: 

        # if currentprice is within offset away from upper limit -> sell 
        if currentPrice > upperLimit - offset:
            return False, True 

        elif currentPrice < lowerLimit + offset: 
            return True, False 

        else: 
            return False, False 
    
    
    else: 
        return False, False


# offset of 0.1 euro works well for above 


# 6

def BreakOut(stock, timeStep): 
    ''''
    Again, a range between min and max. 
    And here, if the stock breaks out above the max, buy and sell as soon as it falls again. 


    For this, somehow the agent has to decide on what to do 


    You have to check this again!!!!
    '''
    dayRange = 10
    dT = 1/24
    rangeLimit = 10
    offset = 0.1
    otherUpperLimit = 1 

    currentPrice = stock[timeStep]

    if int(dayRange * 1/dT) > timeStep: 
        return False, False, currentPrice * 10e6
            
    # we want to break out of the range!! 
    arrayOfInterest = stock[timeStep - int(dayRange * 1/dT): timeStep]
    # stock[timeStep - int((dayRange + 1) * 1/dT): timeStep - int((1) * 1/dT)]

    # look at maximum of this part of the stock 
    upperLimit = np.max(arrayOfInterest)

    # find min in array (lower range limit)
    lowerLimit = np.min(arrayOfInterest)

    # if there exists a range within the margin we defined 
    if upperLimit - lowerLimit < rangeLimit: 

        # if currentprice is within offset away from upper limit -> sell 
        if currentPrice > upperLimit:
            return True, False, upperLimit

        elif currentPrice <= otherUpperLimit: 
            return False, True, upperLimit

        else: 
            return False, False, upperLimit
    
    else: 
        return False, False, upperLimit


# EXAMPLE FOR BREAKOUTTRADING

# NUMBEROFDAYS = 300

# INITIALPRICE = 100  # Initial stock price
# DRIFT = 0.0001       # Drift term
# VOLATILITY = 0.01  # Volatility term

# DT = 1/24

# stock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)

# buyList = []
# sellList = []

# asdf = 0

# for timeStep in range(len(stock)):
#     print(timeStep)
#     buy, sell, asdf = BreakOut(stock, 3, DT, 10, 0.1, timeStep, asdf)

#     buyList.append(buy)
#     sellList.append(sell)

# print(buyList.count(True), buyList.count(False))
# print(sellList.count(True), sellList.count(False))

# ShowStock(stock, False, 0, True, [10])

# exit()


# def IntraDayMeanReversion(stock, timeStep): 
#     return None 


# def MomentumStrategy(stock, timeStep): 
#     '''
#     Buy when 2nd derivative == 0
#     '''




# 7

def ReversalTrading(stock, timeStep): 
    '''
    If it has been falling for a long time and now starts rising again -> buy 

    Essentially the same as scalping somehow

    '''
    timeA = 10
    timeB = 10


    buy = True
    sell = True

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



# 8

def BuyMorningSellNight(stock, timeStep): 
    '''
    Easy strategy where we buy every morning and sell every night 
    '''
    numberOfDays = 300

    dayLength = int(len(stock) / numberOfDays)

    buy = False
    sell = False

    # morning
    if timeStep % dayLength == 0: 
        buy = True

    # night
    if timeStep % (dayLength) == 1: 
        sell = True

    return buy, sell



# 9

def BuyAndSellRandomly(stock, timeStep): 
    '''
    Buy at random times and sell at random times. 
    Independent of the timestep or anything else. 
    '''
    thresHoldProbability = 0.01

    randomNumberBuy = random.random()
    randomNumberSell = random.random()

    if randomNumberBuy < thresHoldProbability: 
        return True, False

    if randomNumberSell < thresHoldProbability: 
        return False, True
    


    return False, False 






# 10

def Scalping(stock, timeStep): 
    '''
    stock has been rising for a certain short time (timeA)  -> buy 
    stock has been rising for a long time (timeB)           -> sell

    timeA and timeB are given in timeSteps

    timeA and timeB could be around 10 timesteps
    '''
    timeA = 5 #10
    timeB = 5 #10

    buy = True
    sell = True

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



