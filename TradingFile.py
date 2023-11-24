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





def Trading(stock, TradingStrategy, numberOfHoldsAtTheSameTime, taxFactor = 0.25): 

    # list of prices where the player bought a stock -> possible to hold more than one stock at a time 
    buyList = []

    # list of prices where a player sold a stock 
    sellList = []

    # iterate over Stock -> each element, because each element in the stock is a possible time to buy or sell (for certain trading strategies)
    for timeStep in range(len(stock)): 

        currentPrice = stock[timeStep]


        # for now, sell decision is independent of value of buyPrice!!
        buy, sell = TradingStrategy(stock, ...)
    
        if buy: 
            buyList.append(currentPrice)

        if sell and len(sellList) < len(buyList): 
            sellPrice = currentPrice * taxFactor
            sellList.append(sellPrice)


        # number of stocks we hold: 
        numStocksHeld = int(len(buyList) - len(sellList))

        # if we reached the end of the stock 
        if timeStep == len(stock)-1: 

            # sell all stocks for the current price 
            for i in range(numStocksHeld): 
                sellList.append(currentPrice)


    profit = 0

    for i in range(len(buyList)): 
        tempProfit = sellList[i] - buyList[i]

        profit += tempProfit


    return profit
            


