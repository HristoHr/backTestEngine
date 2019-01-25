import time
import pandas as pd
import sqlite3
import multiprocessing
import pprint
import itertools

startTimer = time.time()

dbName = "bitfinex"
dcmTS = 1
priceIndex = 1
if dbName == "kraken":
    dcmTS = 10000
    priceIndex = 2
elif dbName == "bitfinex":
    dcmTS = 1000
    priceIndex = 2
# print("historySize, candleSize, ATRFilterHigh, ATRFilterLow, profitTarget, lossTarget,loosingTrades,profitableTrades,totalTrades,finalEquity,profit")

conn = sqlite3.connect(dbName + ".db")
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_BTC_LTC WHERE ts >=? AND ts<=?", (1483228800 * dcmTS, 1545472800 * dcmTS))
results = cur.fetchall()

tStart = (round(results[0][0] / dcmTS))
tEnd = (round(results[len(results) - 1][0] / dcmTS))
start = tStart - (tStart % 3600) - 3 * 3600
end = tEnd - (tEnd % 3600) + 3 * 3600
# print("start", tStart)
# print("end", tEnd)
index = 0
price = 0
candleSize = 60
historySize = 24
roundDec = 5
makerFee = 0.00 / 100
takerFee = 0.03 / 100
candleList = []

for i in range(start, end, 120 * candleSize):
    tup = ((i - 60 * candleSize), i)
    candleList.append(tup)
    index += 1


candleOpenTime = (candleList[0][0])
candleCloseTime = (candleList[0][0])


def backTest(params):
    profitTarget = params[0] / 10000
    lossTarget = params[1] / 10000
    ATRFilterHigh = params[2] / 10000
    ATRFilterLow = params[3] / 10000
    listQC = []
    lastTs = 0
    startEquityCurrency = 10
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
    candleSize = 60
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
                        SMALow = round(sum(candleLowList) / len(candleLowList), roundDec)
                        SMAHigh = round(sum(candleHighList) / len(candleHighList), roundDec)
                        # SMA = round(sum(candleCloseList) / len(candleCloseList), roundDec)
                        ATR = round((SMAHigh - SMALow), roundDec)

                        DCLow = round(DCLowList[-1], roundDec)
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
                        openBuyPrice = price + 0.00001
                        equityAsset = 0.01 * equityCurrency / openBuyPrice
                        if (equityCurrency > equityAsset * openBuyPrice):
                            profitPrice = openBuyPrice + profitTarget
                            lossPrice = openBuyPrice - lossTarget

                            profitFee = openBuyPrice * makerFee + profitPrice * takerFee
                            lossFee = openBuyPrice * takerFee + lossPrice * takerFee

                            potentialProfit = equityAsset * (profitTarget - profitFee)
                            potentialLoss = equityAsset * (lossTarget + lossFee)
                            action = "closeBuy"

                if (action == "closeBuy"):
                    if (price > profitPrice):
                        action = "sell"
                        profitableTrades += 1
                        equityCurrency += potentialProfit
                    elif (price < lossPrice):
                        action = "sell"
                        loosingTrades += 1
                        equityCurrency -= potentialLoss

    totalTrades = loosingTrades + profitableTrades
    # profit = round((((equityCurrency - startEquityCurrency) / startEquityCurrency) * 100), 2)
    profit = equityCurrency - startEquityCurrency
    if (totalTrades > 0):
        print("profitTarget", profitTarget, "lossTarget", lossTarget, "ATRHight", "ATRFilterHigh", ATRFilterHigh,
              "ATRFilterLow", ATRFilterLow)
        print("ATRHigh:", ATRFilterHigh, "ATRLow:", ATRFilterLow,
              "profitTarget:", profitTarget, "lossTarget:", lossTarget,
              "loosingTrades:", round((loosingTrades / totalTrades) * 100, 2),
              "profitableTrades:", round((profitableTrades / totalTrades) * 100, 2), "totalTrades:", totalTrades,
              "equityCurrency:", equityCurrency, "profit:", profit)
    else:
        print("NULL")


processes = 3
pool = multiprocessing.Pool(processes=processes)

profitTarget = range(5, 9, 1)  # [0.0005, 0.0005, 0.0005]  #
lossTarget = range(5, 6, 1)  # range(5, 25, 5)
ATRHight = range(7, 8, 1)  # range(5, 11, 1)
ATRLow = range(2, 3, 1)  # range(1, 5, 1)
# geomP = range (1,3,1)
print(profitTarget)
paramList = list(itertools.product(profitTarget, lossTarget, ATRHight, ATRLow))
print(paramList)
pool.map(backTest, paramList)
endTimer = time.time()

print("processes", processes, "Time to complete: ", (endTimer - startTimer))
