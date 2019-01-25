import sqlite3
import time
import pandas as pd

exchangeList = ["bitfinex", "kraken", "gdax"]

# for exchange in exchangeList:
equityCurrency = 5000
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
profitTarget = 0
lossTarget = 0
candleSize = 15
historySize = 20
potentialLoss = 0
potentialProfit = 0
profitWantedDefault = 0.001
lossWantedDefault = 0
profitWanted = 0
ATRFilterLow = 0.0000
ATRFilterHigh = 100
ATRList = []
DCLowList = []
candleOpenList = []
candleCloseList = []
SMA = 0
SMALow = 0
SMAHigh = 0
candleVolume = 0
ATRDict = {}
feeList = []
makerFee = 0.03 / 100
takerFee = 0.00 / 100
geomP = 2
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
candleList = []
totalCandles = 0
missingCandlesCount = 0
totalCandlesCount = 0
candleClosePrice = 0

# for i in range(10, 500, 20):000
#     key = str((i - 10)) + ":" + str(i)
#     ATRDict[key] = 0

dbName = "kraken"
dcmTS = 1
priceIndex = 1
if dbName == "kraken":
    dcmTS = 10000
    priceIndex = 2
elif dbName == "bitfinex":
    dcmTS = 1000
    priceIndex = 2

conn = sqlite3.connect(dbName + ".db")
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_BTC_LTC WHERE ts >=?", (1483228800 * dcmTS,))
results = cur.fetchall()
# ts = (results[0][0])
# print(ts)
start = round(1483228800) + 60 * candleSize
for i in range(start, 1546214400, 60 * candleSize):
    candleList.append(i)
    print(i)

index = 0
price = 0

while index in range(0, len(results) - 1):
    ts = round(int(results[index][0]) / dcmTS)
    price = (float(results[index][priceIndex]))
    # volume = float(row[2])
    # print(ts)
    # print(i)
    # candleOpenTime = ts
    # candleOpenPrice = volume
    # totalCandles = len(candleList)
    # print(time.strftime("%d %b %Y %H:%M:%S", time.localtime(candleOpenTime)))
    # print(candleOpenPrice)
    candleOpen = candleList[totalCandlesCount]
    candleClose = candleList[totalCandlesCount + 1]
    candleNextOpen = candleList[totalCandlesCount + 2]
    # print("candleOpen", candleOpen)
    # print("candleClose", candleClose)
    # print(ts)
    if ((ts >= candleOpen) and (ts < candleClose)):
        candlePricesList.append(price)
    elif (ts >= candleClose):
        totalCandlesCount += 1
        if (len(candlePricesList) > 0):
            candleOpenPrice = candlePricesList[0]
            candleClosePrice = candlePricesList[-1]
            candleLowPrice = min(candlePricesList)
            candleHighPrice = max(candlePricesList)

            candleLowList.append(candleLowPrice)
            candleHighList.append(candleHighPrice)
            candleCloseList.append(candleClosePrice)

            createdCandlesCount += 1
            candlePricesList.clear()
            # candlePricesList.append(candleClosePrice)

            if (createdCandlesCount >= historySize):
                SMALow = (sum(candleLowList) / len(candleLowList))
                SMAHigh = (sum(candleHighList) / len(candleHighList))
                SMA = (sum(candleCloseList) / len(candleCloseList))
                ATR = (SMAHigh - SMALow)

                DCLowList.append((min(candleLowList)))
                DCLow = DCLowList[len(DCLowList) - 1]
                DCHigh = (max(candleHighList))
                DCMid = (DCHigh - DCLow)

                candleLowList.pop(0)
                candleHighList.pop(0)
                candleCloseList.pop(0)
        #
    else:
        index += -1
        #     # print(candleList[totalCandlesCount], "-", candleList[totalCandlesCount + 1])
        #     missingCandlesCount += 1
        #     createdCandlesCount = 0
        #     canceledTrades += 1
        #     equityAsset = 0
        #     SMALow = 0
        #     SMAHigh = 0
        #     SMA = 0
        #     ATR = 0
        #     DCLowList.clear()
        #     DCLow = 0
        #     DCHigh = 0
        #     DCMid = 0
        #     action = "cancelBuy"
        # candlePricesList.clear()
        # candleLowList.clear()
        # candleHighList.clear()
        # candleOpenList.clear()


    # if (createdCandlesCount >= historySize):

    # if (equityCurrency / openBuyPrice >= equityAsset):
    #     # potentialRatio = potentialProfit / potentialLoss
    #     # wantedRatio = profitWantedDefault / lossWantedDefault
    #     # if (potentialRatio >= 8 / 13):
    #     #     feeHigh += 1
    #     # else:
    #
    #
    #     # print("Open Buy at:", openBuyPrice)
    #     # print("Wanted Profit:", profitWanted)
    #     continue
    # else:
    #     notEnoughCurrency += 1
    #     print("Not Enough $$$")
    #     continue
    # print("Not Enough Asset !!!")
    # print("openBuyPrice", openBuyPrice)
    if (createdCandlesCount >= historySize):
        if (action == "sell" or action == "cancelBuy"):
            if (price < DCLow):
                profitTarget = ATR
                lossTarget = ATR
                openBuyPrice = price  # round(candleOpen - 1.5 * ATR, 2)
                # print("price", price)
                # print("ATR", ATR)
                # print("SMA", SMA)
                # print("candleClosePrice", candleClosePrice)
                # print("candleLowPrice", candleLowPrice)
                # print("DCLow", DCLow)
                # # print("SMAHigh", SMAHigh)
                # print("openBuyPrice", openBuyPrice)
                # profitWanted = profitWantedDefault * 2 ** inRow
                # equityAsset = profitWanted / profitTarget

                profitPrice = openBuyPrice + profitTarget
                lossPrice = openBuyPrice - lossTarget

                profitFee = openBuyPrice * makerFee + profitPrice * makerFee
                lossFee = openBuyPrice * makerFee + lossPrice * takerFee
                #
                # potentialProfit = equityAsset * (profitTarget - profitFee)
                # potentialLoss = equityAsset * (lossTarget + lossFee)
                #
                # assetTradeList.append(equityAsset)
                # currencyTradeList.append(equityAsset * price)
                # feeList.append(lossFee * equityAsset)
                action = "closeBuy"

        if (action == "openBuy"):
            if (price < openBuyPrice):
                action = "closeBuy"
                # print("closeBuy", price)
                # print("Asset bought:", equityAsset)
                # print("Equity Fiat:", equityCurrency)


            elif (price > DCLow):  # or ATR > ATRFilterHigh):  # and ATR > ATRFilterHigh and ATR < ATRFilterLow):
                action = "cancelBuy"
                canceledTrades += 1
                # print("Canceled", price)

        if (action == "closeBuy"):
            if (price > profitPrice):
                action = "sell"
                profitableTrades += 1
                equityCurrency += potentialProfit
                inRow += 1
                if (inRow == geomP):
                    inRow = 0
                    hit += 1
                # print("Profit", price)

            elif (price < lossPrice):
                action = "sell"
                loosingTrades += 1
                equityCurrency -= potentialLoss
                inRow = 0
                # print("Loss", price)

        # feeList = openBuyPrice * makerFee + profitPrice * makerFee
        # print("candleLow", candleLow)
    index += 1
totalTrades = profitableTrades + loosingTrades
# print("Bad trades:", badTrades / (totalTrades + badTrades) * 100, "%")
print("Canceled trades:", canceledTrades)
print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
print("Total trades:", totalTrades)
print("Final equity Currency:", equityCurrency)
print("Hits:", hit)
print("Fee too high:", feeHigh)
print("Not Enough Currency", notEnoughCurrency)
print("Geometric Progression:", geomP)
# print("Max Asset needed", max(assetTradeList))
# print("Max Currency needed", max(currencyTradeList))
# print("Avr Asset needed", sum(assetTradeList) / len(assetTradeList))
# print("Avt Currency needed", sum(currencyTradeList) / len(assetTradeList))
# print("Max Fee", max(feeList))
# print("Avr Fee", sum(feeList) / len(feeList))
print("Missing Candles", missingCandlesCount)
print("Created Candles", createdCandlesCount)
print("Total Candles", totalCandlesCount)
print("Bad Trades", badTrades)
# for key, value in ATRDict.items():
#     print(key + "-" + str(round(value / 1000)))
