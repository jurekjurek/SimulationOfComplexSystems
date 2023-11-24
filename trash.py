def MovingAverage(stockEvolution, daysConsidered, dT, sellFactor ): 
    '''
    this function takes into account the last n days of the stock market 
    '''

    avg = 0

    stepsPerDay = int( 1 / dT)

    lower = False
    buy = False

    # consider last few days
    for dayNo in range(daysConsidered): 

        # sum up closing prices over days 
        avg += stockEvolution[int( dayNo * int(1/dT) )]

    avg /= daysConsidered


    buyPrices = []
    sellPrices = []

    for i in range(len(stockEvolution)):

        # update Avg
        if i%stepsPerDay == 0: 

            dayNo = int( num_days / i )

            partOfArray = stockEvolution[i: (dayNo + daysConsidered) * stepsPerDay]

            # calculate average over every stepsperday-th element 
            avg = np.mean(partOfArray[:: stepsPerDay ].reshape(-1, stepsPerDay), axis=1)


        if stockEvolution[i] < avg: 
            lower = True
        
        if stockEvolution[i] >= avg and lower == True: 
            buyPrice = stockEvolution[i]
            buy = True
            lower = False 
            buyPrices.append(buyPrice)

        if buy == True and stockEvolution[i] < avg * sellFactor: 
            buy = False 
            lower = True
            sellPrice = stockEvolution[i]
            sellPrices.append(sellPrice)


        # if last element -> sell 

        if i == len(stockEvolution): 
            sellPrice = stockEvolution[i]
            sellPrices.append(sellPrice)

    return buyPrices, sellPrices 