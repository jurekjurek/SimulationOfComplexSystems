'''
In this file, we have a function that takes a simulated stock and a trading strategy. 

All the trading strategy functions return True or False, indicating if it is a good idea to buy (or sell) given 
the day and the stock and of course, the trading strategy that is follow. 

Buy and Hold for instance will return False always, unless we reached the last end of the time period that was simulated. 



'''
from TradingStrategies import * 
from stocks import *

def MainSimulation(numberOfHoldsAtTheSameTime): 

    # create simulated stock 
    stock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)


    profit1 = Trading(stock, BuyAndHold, numberOfHoldsAtTheSameTime)

    profit2 = Trading(stock, BuyAndHold, numberOfHoldsAtTheSameTime)





def Trading(stock, TradingStrategy, allowHoldsAtTheSameTime, maxBuys, dT, taxFactor = 0.25): 

    # list of prices where the player bought a stock -> possible to hold more than one stock at a time 
    buyList = []

    # list of prices where a player sold a stock 
    sellList = []

    sellIndicesList = []

    # variables inside function, probably not a good idea 
    dayRange = 10
    dayRangeLong = 10
    dayRangeShort = 5

    rangeLimit = 20
    rangeOffset = 0.5

    scalpingTimeA = 1
    scalpingTimeB = 1



    # iterate over Stock -> each element, because each element in the stock is a possible time to buy or sell (for certain trading strategies)
    for timeStep in range(len(stock)): 

        currentPrice = stock[timeStep]


        # for now, sell decision is independent of value of buyPrice!!
        # buy, sell = TradingStrategy(stock, ...)

        # take a look at all the trading strategies: 
        if TradingStrategy == 'MovingAverage': 
            buy, sell = MovingAverage(stock, timeStep, dayRange, dT, 20)

        elif TradingStrategy == 'BuyAndHold': 
            buy, sell = BuyAndHold(stock, timeStep)
        # elif TradingStrategy == 'ExponentialMovingAverage': 
        #     buy, sell = ExponentialMovingAverage(stock, timeStep)
        elif TradingStrategy == 'CrossoverMovingAverage': 
            buy, sell = CrossOverMovingAverage(stock, timeStep, dayRangeLong, dayRangeShort, dT)
        elif TradingStrategy == 'MeanReversion':
            buy, sell = MeanReversion(stock, timeStep, dT, dayRange)
        elif TradingStrategy == 'RangeTrading': 
            buy, sell = RangeTrading(stock, dayRange, dT, rangeLimit, rangeOffset, timeStep)
        elif TradingStrategy == 'BreakOut':
            buy, sell = BreakOut(stock, dayRange, dT, rangeLimit, rangeOffset, timeStep)
        elif TradingStrategy == 'BuyMorningSellNight': 
            buy, sell = BuyMorningSellNight(stock, timeStep, dT)
        elif TradingStrategy == 'Scalping': 
            buy, sell = Scalping(stock, timeStep, scalpingTimeA, scalpingTimeB)
        elif TradingStrategy == 'BuyAndSellRandomly':
            buy, sell = BuyAndSellRandomly(stock, timeStep, 4e-3)



    
        if buy and len(buyList) <= maxBuys: 
            if allowHoldsAtTheSameTime: 
                buyList.append(currentPrice)
            elif len(buyList) == len(sellList): 
                buyList.append(currentPrice)

        if sell and len(sellList) < len(buyList): 
            sellPrice = currentPrice

            # look at taxes. If we made profit, there's taxes on the profit. 
            correspondingBuyPrice = buyList[len(sellList)-1]

            if sellPrice > correspondingBuyPrice:
                diff = sellPrice - correspondingBuyPrice
                sellPrice = correspondingBuyPrice + taxFactor * diff

            sellList.append(sellPrice)
            sellIndicesList.append(timeStep)


        # number of stocks we hold: 
        numStocksHeld = int(len(buyList) - len(sellList))

        # if we reached the end of the stock 
        if timeStep == len(stock)-1: 

            # sell all stocks for the current price 
            for i in range(numStocksHeld): 
                sellList.append(currentPrice)
                sellIndicesList.append(timeStep)


    profit = 0

    for i in range(len(buyList)): 
        tempProfit = sellList[i] - buyList[i]

        profit += tempProfit


    return profit, buyList, sellList, sellIndicesList
            

stock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)

profit, buyList, sellList, sellListIndices = Trading(stock, 'MovingAverage', False, 1, DT)

print(buyList, sellList)
print(profit)



# def ShowStock(stock, showZ, dayRangeZ, showMA, dayRange1, dayRange2):

#     plt.plot(stock)


#     averageList10 = []
#     averageList5 = []
#     zScoreList = []
#     daysList = np.arange(NUMBEROFDAYS) * 1/DT

#     for i in range(NUMBEROFDAYS):

#         zScoreList.append(CalculateZScore(stock, i, DT, dayRangeZ))
#         averageList10.append(CalculateMovingAverage(stock, i, DT, dayRange1, True))
#         averageList5.append(CalculateMovingAverage(stock, i, DT, dayRange2, True))

#     if showMA: 
#         plt.plot(daysList, averageList10, label = 'Moving Average, ' + str(dayRange1))
#         plt.plot(daysList, averageList5, label = 'Moving Average, ' + str(dayRange2))
#         plt.xlim((dayRange1 * 1/DT, daysList[-1]))

#     # plt.scatter(np.where(stock == buyList[0]), buyList[0], color = 'orange', label = 'Buy')
#     # plt.scatter(sellListIndices[0], stock[sellListIndices[0]], color = 'black', label = 'Sell')
#     plt.title('Stocks simulated using GBM')
#     plt.xlabel('Time [h]')
#     plt.ylabel('Price')
    
#     plt.legend()
#     plt.show()

#     if showZ: 
#         # plot Z value 
#         plt.plot(daysList, zScoreList, label = 'Z-Score, ' + str(dayRangeZ))
#         plt.title('Evolution of the Z-Value')
#         plt.xlabel('Time [h]')
#         plt.ylabel('Z-Value')
#         plt.legend()
#         plt.show()

