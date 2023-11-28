class Agent:
    def __init__(self, initial_money, trading_strategy):
        self.money = initial_money
        self.portfolio = {}  # Dictionary to store stock holdings, e.g., {'AAPL': 10, 'GOOGL': 5}
        self.trading_strategy = trading_strategy

    def take_action(self, current_price, available_stocks):
        action = self.trading_strategy.decide_action(current_price, self.money, self.portfolio, available_stocks)
        if action['type'] == 'buy':
            self.buy(action['stock'], action['quantity'], current_price)
        elif action['type'] == 'sell':
            self.sell(action['stock'], action['quantity'], current_price)

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
