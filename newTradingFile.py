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


# MainSimulation(INITIALMONEY, BuyAndSellRandomly, True)



def CompareTradingStrategies(initialMoney, holdsAtOnce): 

    # one stock (for now, only one) that all agents with all different trading strategies will follow 
    globalStock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)

    # define different agents for all 10 (9) trading strategies: 

    agentBAH = Agent(initialMoney, BuyAndHold, globalStock, holdsAtOnce=holdsAtOnce)

    agentMA = Agent(initialMoney, MovingAverage, globalStock, holdsAtOnce=holdsAtOnce)

    agentCO = Agent(initialMoney, CrossOverMovingAverage, globalStock, holdsAtOnce=holdsAtOnce)

    agentMR = Agent(initialMoney, MeanReversion, globalStock, holdsAtOnce=holdsAtOnce)

    agentRT = Agent(initialMoney, RangeTrading, globalStock, holdsAtOnce=holdsAtOnce)

    agentBO = Agent(initialMoney, BreakOut, globalStock, holdsAtOnce=holdsAtOnce)

    agentRV = Agent(initialMoney, ReversalTrading, globalStock, holdsAtOnce=holdsAtOnce)

    agentMN = Agent(initialMoney, BuyMorningSellNight, globalStock, holdsAtOnce=holdsAtOnce)

    agentSC = Agent(initialMoney, Scalping, globalStock, holdsAtOnce=holdsAtOnce)

    agentRandom = Agent(initialMoney, BuyAndSellRandomly, globalStock, holdsAtOnce=holdsAtOnce)  

    agentList = [agentBAH, agentMA, agentCO, agentMR, agentRT, agentRV, agentMN, agentSC, agentRandom]


    # list to store the profits that certain agents make following a certain strategy 
    profitList = []

    for timeStep in range(len(globalStock)):

        for agent in agentList: 

            agent.take_action(timeStep, globalStock)

        
    for agent in agentList: 

        while len(agent.sellList) < len(agent.buyList): 
            agent.sell(globalStock, timeStep, agent.taxFactor)
        
        profitList.append(agent.money - initialMoney)


    # show a histogram of money of agents: 

    print(profitList)

    namesList = ['BuyAndHold', 'MovingAverage', 'Crossover', 'MeanReversion', 'Rangetrading', 'Reversal', 'MorningNight', 'Scalping', 'Random']

    plt.bar(namesList ,profitList)
    plt.title('Comparison of profits with different trading strategies')
    plt.ylabel('Profit')
    plt.xlabel('Trading Strategy')
    plt.xticks(fontsize = 5)
    plt.show()


CompareTradingStrategies(1000, 10)



