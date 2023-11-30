from TradingStrategies import * 
from stocks import *
from AgentClass import * 


# global variables 
NUMBEROFDAYS = 100

INITIALPRICE = 100  # Initial stock price
DRIFT = 0.0001       # Drift term
VOLATILITY = 0.01  # Volatility term
NUMBEROFSIMULATIONS = 5  # Number of simulations

DT = 1/24

# initial money for agent 
initialMoney = 1000

def MainSimulation(initialMoney, tradingStrategy, show): 

    stock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)

    # define agent 
    agent = Agent(initialMoney, tradingStrategy, stock, oneBuyOnly=True)

    for timeStep in range(len(stock)): 

        agent.take_action(timeStep, stock)

    while len(agent.sellList) < len(agent.buyList): 
        agent.sell(stock, timeStep, agent.taxFactor)

    print(agent.buyList)
    print(agent.sellList)

    if show: 
        for i in range(len(agent.buyList)):
            plt.scatter(agent.buyList[i], stock[agent.buyList[i]], s= 200, label = 'Buy')
            plt.scatter(agent.sellList[i], stock[agent.sellList[i]], s=200, label = 'Sell')
        ShowStock(stock, False, 0, True, [5, 20], NUMBEROFDAYS, DT)
        # plt.plot(stock)
        # plt.legend()
        plt.show()

MainSimulation(100, CrossOverMovingAverage, True)