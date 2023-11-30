'''
Write class for agent 
'''
from TradingStrategies import *


class Agent:
    def __init__(self, initial_money, trading_strategy, stock, oneBuyOnly):
        self.money = initial_money

        # portfolio right now is just a counter of stocks held 
        self.portfolio = [] #{}  # Dictionary to store stock holdings, e.g., {'AAPL': 10, 'GOOGL': 5}
        self.trading_strategy = trading_strategy
        self.stock = stock
        self.taxFactor = 0.25
        self.oneBuyOnly = oneBuyOnly
        
        # buy and sell list for agent to check when they bought and sold, keep track of timesteps
        self.buyList = []
        self.sellList = []

    def take_action(self, timeStep, stock):
        buy, sell = self.trading_strategy(stock, timeStep)
        if buy == True:
            self.buy(stock, timeStep)
        elif sell == True:
            self.sell(stock, timeStep, self.taxFactor)

    def buy(self, stock, timeStep):
        currentPrice = stock[timeStep]
        if self.oneBuyOnly == True and len(self.portfolio) >= 1: 
            return 

        if self.money >= currentPrice:
            self.money -= currentPrice

            # increase number of stocks held by one 
            self.portfolio.append(currentPrice)

            self.buyList.append(timeStep)
        else: 
            print('No money left to make this transaction.')

    def sell(self, stock, timeStep, taxFactor):
        if self.portfolio != []:
            currentPrice = stock[timeStep]

            profit = currentPrice - self.portfolio[0]

            if profit > 0: 
                self.money += self.portfolio[0] + profit * (1-taxFactor)

            else: 

                self.money += currentPrice

            # erase the stock from the portfolio 

            del self.portfolio[0]

            self.sellList.append(timeStep)
