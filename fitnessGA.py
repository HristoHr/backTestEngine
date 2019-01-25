import numpy
import itertools
import multiprocessing
import functools
import random
import copy

fitnessList = []
candleList = []
results = []
candleSize = 60
historySize = 24
roundDec = 5
dbName = "bitfinex"
dcmTS = 1
priceIndex = 1
if dbName == "kraken":
    dcmTS = 10000
    priceIndex = 2
elif dbName == "bitfinex":
    dcmTS = 1000
    priceIndex = 2


def cal_pop_fitness(population, candleList, results):
    parents = []
    offspring = []
    for i in range(0, len(population)):
        if population[i][0] > 0:
            parents.append(population[i])
        else:
            offspring.append(population[i])
    processes = 2
    pool = multiprocessing.Pool(processes=processes)
    funct = functools.partial(back_test, candleList=candleList, results=results)
    fitnessList = pool.map(funct, offspring)

    for j in range(0, len(parents)):
        fitnessList.append(parents[j])
    return fitnessList

    # indexedPop = copy.deepcopy(population)
    # for i in range(0, len(indexedPop)):
    #     indexedPop[i].insert(0, i)
    #
    # print(population)
    # print(indexedPop)

    # profitTarget = range(5, 6, 1)  # [0.0005, 0.0005, 0.0005]  #
    # lossTarget = range(5, 6, 1)  # range(5, 25, 5)
    # ATRHight = range(7, 8, 1)  # range(5, 11, 1)
    # ATRLow = range(2, 3, 1)  # range(1, 5, 1)
    # # geomP = range (1,3,1)

    # candleList = candle_list
    # results = results_
    # for i in range(0, len(pop)):
    #     print(pop[i])# + (candleList,) + (results,))
    #     params.append(pop[i] + (candleList,) + (results,))
    # pop.tolisst()
    # map(functools.partial(add, y=2), a)

    # print(fitness)
    # print(new_population_list)
    # print(params[1])
    # print(params[2])
    # fitnessTupList.sort()
    # for tup in fitnessTupList:
    # fitnessList.append(tup.pop(1))


def select_mating_pool(population, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    population = numpy.array(population)
    parents = numpy.empty((num_parents, population.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = population[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99
    return parents


def crossover(parents):
    offspring = []
    for subset in itertools.combinations(parents, 2):
        parent1Profit = subset[0][0]
        parent1ProfitTarget = subset[0][1]
        parent1LossTarget = subset[0][2]
        parent1ATRHight = subset[0][3]
        parent1ATRLow = subset[0][4]

        parent2Profit = subset[1][0]
        parent2ProfitTarget = subset[1][1]
        parent2LossTarget = subset[1][2]
        parent2ATRHight = subset[1][3]
        parent2ATRLow = subset[1][4]

        chiildProfitTarget = (parent1Profit * parent1ProfitTarget + parent2Profit * parent2ProfitTarget) / (
                parent1Profit + parent2Profit)
        childLossTarget = (parent1Profit * parent1LossTarget + parent2Profit * parent2LossTarget) / (
                parent1Profit + parent2Profit)
        childATRHight = (parent1Profit * parent1ATRHight + parent2Profit * parent2ATRHight) / (
                parent1Profit + parent2Profit)
        childATRLow = (parent1Profit * parent1ATRLow + parent2Profit * parent2ATRLow) / (parent1Profit + parent2Profit)
        candleSize = random.choice(
            [15, 30, 60])  # (parent1Profit*parents[i][5] + parent2Profit*parents[i+1][5])/parent1Profit+parent2Profit

        offspring.append(
            [-99, round(chiildProfitTarget, roundDec), round(childLossTarget, roundDec),
             round(parent1ATRHight, roundDec),
             round(parent1ATRLow, roundDec), candleSize])
        offspring.append(
            [-99, round(chiildProfitTarget, roundDec), round(childLossTarget, roundDec),
             round(parent2ATRHight, roundDec),
             round(parent2ATRLow, roundDec), candleSize])
        offspring.append(
            [-99, round(parent1ProfitTarget, roundDec), round(parent1LossTarget, roundDec),
             round(childATRHight, roundDec),
             round(childATRLow, roundDec), candleSize])
        offspring.append(
            [-99, round(parent2ProfitTarget, roundDec), round(parent2LossTarget, roundDec),
             round(childATRHight, roundDec),
             round(childATRLow, roundDec), candleSize])

    for parent in parents:
        offspring.append(parent)
        # offspring = numpy.empty(offspring_size)
    # # The point at which crossover takes place between two parents. Usually it is at the center.
    # crossover_point = numpy.uint8(offspring_size[1] / 2)
    #
    # for k in range(offspring_size[0]):
    #     # Index of the first parent to mate.
    #     parent1_idx = k % parents.shape[0]
    #     # Index of the second parent to mate.
    #     parent2_idx = (k + 1) % parents.shape[0]
    #     # The new offspring will have its first half of its genes taken from the first parent.
    #     offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
    #     # The new offspring will have its second half of its genes taken from the second parent.
    #     offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]

    return offspring


# def mutation(offspring_crossover):
#     # Mutation changes a single gene in each offspring randomly.
#     for idx in range(offspring_crossover.shape[0]):
#         # The random value to be added to the gene.
#         random_value = numpy.random.randint(1, 10, 1)
#         offspring_crossover[idx, 0] = offspring_crossover[idx, 0] + random_value
#     return offspring_crossover


def back_test(params, candleList, results):
    # print("candleList", params[0])
    # print("results", params[1])
    # print("values", params[2])
    # print(params)
    # processOrder = params[0]
    profitTarget = params[1]
    lossTarget = params[2]
    ATRFilterHigh = params[3]
    ATRFilterLow = params[4]
    candleSize = params[5]
    # candleList = params[4]
    # results = params[5]
    # print(params
    listQC = []
    lastTs = 0
    initialEquityCurrency = 10
    equityCurrency = 10
    equityAsset = 0
    createdCandlesCount = 0
    candleOpenTime = 0
    candleOpen = 0
    candleCloseTime = 0
    candleClose = 0
    candleLowPrice = 0
    canceledTrades = 0
    candleHigh = 0
    candlePricesList = []
    candleLowList = []
    candleHighList = []
    ATR = 0
    action = "sell"
    openBuyPrice = 0
    loosingTrades = 0
    profitableTrades = 0
    badTrades = 0
    profit = 0
    profitRow = 0
    candleHighestList = []
    candleLowestList = []

    historySize = 24
    potentialLoss = 0
    potentialProfit = 0
    profitWantedDefault = 0
    lossWantedDefault = 0
    profitWanted = 0

    ATRList = []
    ATRBuy = 0
    DCLowList = []
    candleOpenList = []
    candleCloseList = []
    SMA = 0
    SMALow = 0
    SMAHigh = 0
    candleVolume = 0
    feeList = []
    makerFee = 0.00 / 100
    takerFee = 0.03 / 100

    inRow = 0
    hit = 0
    feeHigh = 0
    bought = True
    lossFee = 0
    candleOpenPrice = 0
    profitPrice = 0
    lossPrice = 0
    notEnoughCurrency = 0
    assetTradeList = []
    currencyTradeList = []
    DCLow = 0
    DCHigh = 0
    DCMid = 0
    totalCandles = 0
    missingCandlesCount = 0
    totalCandlesCount = 0
    candleClosePrice = 0

    for j in range(1, len(candleList)):
        candleOpenTime = candleCloseTime
        candleCloseTime = (candleList[j][1])
        if (equityCurrency <= 0):
            profit = 0
            break
        for i in range(lastTs, len(results)):
            ts = round(results[i][0] / dcmTS)
            price = round(float(results[i][priceIndex]), roundDec)
            if (ts >= candleOpenTime and ts <= candleCloseTime):
                candlePricesList.append(price)
            elif ts > candleCloseTime:
                if len(candlePricesList) > 0:
                    candleOpenPrice = candlePricesList[0]
                    candleClosePrice = candlePricesList[-1]
                    candleLowPrice = min(candlePricesList)
                    candleHighPrice = max(candlePricesList)

                    candleLowList.append(candleLowPrice)
                    candleHighList.append(candleHighPrice)
                    candleCloseList.append(candleClosePrice)

                    createdCandlesCount += 1
                    DCLowList.append((min(candleLowList)))
                    candlePricesList.clear()
                    # candlePricesList.append(candleClosePrice)
                    if (createdCandlesCount >= historySize):
                        SMALow = sum(candleLowList) / len(candleLowList)
                        SMAHigh = sum(candleHighList) / len(candleHighList)
                        # SMA = round(sum(candleCloseList) / len(candleCloseList), roundDec)
                        ATR = SMAHigh - SMALow

                        DCLow = DCLowList[-1]
                        # DCLow = round(min(candleLowList), roundDec)
                        # DCHigh = round(max(candleHighList), roundDec)
                        # DCMid = round((DCHigh - DCLow), roundDec)

                        candleLowList.pop(0)
                        candleHighList.pop(0)
                        candleCloseList.pop(0)
                lastTs = i
                break
            if (createdCandlesCount >= historySize):
                if (action == "sell" or action == "cancelBuy"):
                    if (price < DCLow and ATR >= ATRFilterLow and ATR <= ATRFilterHigh):
                        openBuyPrice = round(price + 0.00001, roundDec)
                        equityAsset = (0.01 * equityCurrency) / openBuyPrice
                        # if (equityCurrency > equityAsset * openBuyPrice):
                        profitPrice = round(openBuyPrice + profitTarget, roundDec)
                        lossPrice = round(openBuyPrice - lossTarget, roundDec)

                        profitFee = openBuyPrice * takerFee + profitPrice * makerFee
                        lossFee = openBuyPrice * takerFee + lossPrice * takerFee

                        potentialProfit = equityAsset * (profitTarget - profitFee)
                        potentialLoss = equityAsset * (lossTarget + lossFee)
                        action = "closeBuy"

                if (action == "closeBuy"):
                    if (price > profitPrice):
                        profitableTrades += 1
                        equityCurrency += potentialProfit
                        action = "sell"
                    elif (price < lossPrice):
                        loosingTrades += 1
                        equityCurrency -= potentialLoss
                        action = "sell"

    totalTrades = loosingTrades + profitableTrades
    # profit = round((((equityCurrency - initialEquityCurrency) / initialEquityCurrency) * 100), 2)
    profit = equityCurrency - initialEquityCurrency
    # if (totalTrades > 0 and profit > 0):
    #     print("ATRHigh:", ATRFilterHigh, "ATRLow:", ATRFilterLow,
    #           "profitTarget:", profitTarget, "lossTarget:", lossTarget,
    #           "loosingTrades:", round((loosingTrades / totalTrades) * 100, 2),
    #           "profitableTrades:", round((profitableTrades / totalTrades) * 100, 2), "totalTrades:", totalTrades,
    #           "equityCurrency:", equityCurrency, "profit:", profit)
    return [profit, profitTarget, lossTarget, ATRFilterHigh, ATRFilterLow, candleSize]
