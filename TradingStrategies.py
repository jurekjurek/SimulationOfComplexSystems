from stocks import * 










def BuyAndHold(stockEvolution, timeStep): 
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

    if timeStep == len(stockEvolution)-1: 

        # if last possible option to trade, sell 
        sell = True 
        

    return buy, sell 


def MovingAverage(stock, timeStep): 
    '''
    If we notice an upwards or downwards trend in the moving average, buy (sell).
    '''





def ExponentialMovingAverage(stock, timeStep): 
    '''
    
    '''
    return None 

def CrossOverMovingAverage(stock, timeStep): 
    '''
    Use short term and long term average and buy if they cross 
    '''
    return None 


def MeanReversion(stock, timeStep): 
    '''
    Calculate mean over certain timeframe, then calculate standard deviation and Z value indicating if a price is lower or higher than actual value
    
    -> use Z value 

    '''


    return None



def RangeTrading(stockEvolution, dayRange, dT, rangeLimit, offset, timeStep):
    '''
    if the Stock is clearly  - only shortterm!!! - between a min and a max value for the last x timesteps -> buy when high in this range 
    sell when break out of range... (some indicators exist ... )

    buy when at lower range max 
    sell when at higher range max 

    offset is distance from limit. If limit - offset is the current price, we buy. Else we do not. 

    '''

    # look a certain number of timesteps in the past
    # if the max and min value of the array corresponding to this certain timeframe is not significantly larger than some certain range we specified, 
    # buy and view this as a range 

    for iteration in range(len(stockEvolution)): 

        arrayOfInterest = stockEvolution[iteration: iteration + int(dayRange * 1/dT)]

        # find max in array (upper range limit)
        upperLimit = np.max(arrayOfInterest)

        # find min in array (lower range limit)
        lowerLimit = np.min(arrayOfInterest)

        if upperLimit - lowerLimit < rangeLimit: 
            range = True 
        else: 
            range = False
            
    


    return None 


def BreakOut(stock, timeStep): 
    ''''
    Again, a range between min and max. 
    And here, if the stock breaks out above the max, buy and sell as soon as it falls again. 
    '''



def IntraDayMeanReversion(stock, timeStep): 
    return None 


def MomentumStrategy(stock, timeStep): 
    '''
    Buy when 2nd derivative == 0
    '''



def ReversalTrading(stock, timeStep): 
    '''
    If it has been falling for a long time and now starts rising again -> buy 
    '''



def BuyMorningSellNight(stock, timeStep): 
    '''
    Easy strategy where we buy every morning and sell every night 
    '''
    return None 



def BuyAndSellRandomly(stock, timeStep): 
    '''
    Buy at random times and sell at random times. 
    '''
    return None 


def Scalping(stock, timeStep, timeA, timeB): 
    '''
    stock has been rising for a certain short time (timeA)  -> buy 
    stock has been rising for a long time (timeB)           -> sell
    '''


