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
INITIALMONEY = 1000

def MainSimulation(initialMoney, tradingStrategy, show): 

    stock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)

    # define agent 
    agent = Agent(initialMoney, tradingStrategy, stock, holdsAtOnce=5)

    print('how much money does this guy have???', initialMoney)

    for timeStep in range(len(stock)): 

        agent.take_action(timeStep, stock)

    # if the end of the stock is reached and the agent is still holding stocks, sell all the stocks for the current price 
    while len(agent.sellList) < len(agent.buyList): 
        agent.sell(stock, timeStep, agent.taxFactor)

    print(agent.buyList)
    print(agent.sellList)

    if show: 
        for i in range(len(agent.buyList)):
            plt.scatter(agent.buyList[i], stock[agent.buyList[i]], s= 200, color = 'red')#, label = 'Buy')
            plt.scatter(agent.sellList[i], stock[agent.sellList[i]], s=200, color = 'green')#, label = 'Sell')
        ShowStock(stock, False, 0, False, [5, 20], NUMBEROFDAYS, DT, 'Profit: ' + str(agent.money - initialMoney))
        # plt.plot(stock)
        # plt.legend()
        plt.show()
    
    print('current money after trading: ', agent.money)


# def CompareTradingStrategies(): 
#     '''
#     In this function, we compare trading strategies to each other. 
#     We have a parameter holdsAtOnce which indicates how many stocks an agent can hold at the same time 
#     '''


MainSimulation(INITIALMONEY, BuyAndSellRandomly, True)