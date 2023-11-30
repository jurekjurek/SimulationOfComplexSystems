'''
Write class for agent 
'''

class Agent:
    def __init__(self, initial_money, trading_strategy, stock):
        self.money = initial_money
        self.portfolio = {}  # Dictionary to store stock holdings, e.g., {'AAPL': 10, 'GOOGL': 5}
        self.trading_strategy = trading_strategy
        self.stock = stock

    def take_action(self, timeStep, available_stocks):
        buy, sell = self.trading_strategy.decide_action(timeStep, self.money, self.portfolio, available_stocks)
        if buy == True:
            self.buy(self.stock, timeStep)
        elif sell == True:
            self.sell(self.stock, timeStep)

    def buy(self, stock, quantity, current_price):
        cost = quantity * current_price
        if self.money >= cost:
            self.money -= cost
            if stock in self.portfolio:
                self.portfolio[stock] += quantity
            else:
                self.portfolio[stock] = quantity

    def sell(self, stock, quantity, current_price):
        if stock in self.portfolio and self.portfolio[stock] >= quantity:
            revenue = quantity * current_price
            self.money += revenue
            self.portfolio[stock] -= quantity
            if self.portfolio[stock] == 0:
                del self.portfolio[stock]
