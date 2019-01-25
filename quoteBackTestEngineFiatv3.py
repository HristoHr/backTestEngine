import sqlite3
import time
import pandas as pd
import numpy as np

exchangeList = ["gdax"]  # ["bitfinex", "kraken", "gdax"]

# for exchange in exchangeList:
#     ATRDictWin = {}
#     ATRDictLoss = {}
#     startKey = 0
#     endKey = 0

# for i in range(10, 210, 10):
#     endKey = (i / 100000)
#     key = str(startKey) + ":" + str(endKey)
#     startKey = endKey
#     ATRDictWin[key] = 0
#     ATRDictLoss[key] = 0

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
STDEV = 0
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

potentialLoss = 0
potentialProfit = 0
# profitWantedDefault = 0.001
# lossWantedDefault = 0
profitWanted = 0
# ATRFilterLow = 0.0000
# ATRFilterHigh = 1.001
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
riskWanted = 0.02
# geomP = 0
# inRow = 0
# hit = 0
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
DCHighList = []
candleList = []
totalCandles = 0
missingCandlesCount = 0
totalCandlesCount = 0
candleClosePrice = 0
roundDec = 5

# for i in range(10, 500, 20):000
#     key = str((i - 10)) + ":" + str(i)
#     ATRDict[key] = 0

dbName = "gdax"
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
cur.execute("SELECT * FROM quotes_BTC_LTC")  # WHERE ts >=? AND ts<=?", (1483228800 * dcmTS, 1545472800 * dcmTS))
results = cur.fetchall()
tStart = (round(results[0][0] / dcmTS))
tEnd = (round(results[len(results) - 1][0] / dcmTS))
start = tStart - (tStart % 3600) - 3 * 3600
end = tEnd - (tEnd % 3600) + 3 * 3600
print("start", tStart)
print("end", tEnd)
# start = round(round(results[0][0]/10000)/600)*600+1200
# print(start)
index = 0
price = 0
candleSize = 5
historySize = 20
roundDec = 5
makerFee = 0.00 / 100
takerFee = 0.03 / 100
candleList = []
DChit = 0
for i in range(start, end, 120 * candleSize):
    tup = ((i - 60 * candleSize), i)
    candleList.append(tup)
    index += 1
lastTs = 0
listQC = []
candleOpenTime = (candleList[0][0])
candleCloseTime = (candleList[0][0])

for j in range(1, len(candleList)):
    candleOpenTime = candleCloseTime
    candleCloseTime = (candleList[j][1])
    if (equityCurrency <= 0):
        break
    for i in range(lastTs, len(results)):
        ts = round(results[i][0] / dcmTS)
        price = round(float(results[i][priceIndex]), roundDec)
        if (ts >= candleOpenTime and ts <= candleCloseTime):
            # print("candleOpenTime", candleOpenTime)
            # print("candleCloseTime", candleCloseTime)
            # print("ts", ts)
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
                DCHighList.append((min(candleHighList)))
                candlePricesList.clear()
                # candlePricesList.append(candleClosePrice)
                if (createdCandlesCount >= historySize):
                    SMALow = (sum(candleLowList) / len(candleLowList))
                    SMAHigh = (sum(candleHighList) / len(candleHighList))
                    SMA = (sum(candleCloseList) / len(candleCloseList))
                    ATR = ((SMAHigh - SMALow))
                    STDEV = np.std(candleCloseList)
                    DCLow = (DCLowList[-1])
                    DCHigh = (DCHighList[-1])
                    # DCLow = round(min(candleLowList), roundDec)

                    # DCMid = round((DCHigh - DCLow), roundDec)

                    candleLowList.pop(0)
                    candleHighList.pop(0)
                    candleCloseList.pop(0)
            lastTs = i
            break
        if (createdCandlesCount >= historySize):
            # print("price", price)
            # print("ATR", ATR)
            # print("SMA", SMA)
            # print("DCLow", DCLow)
            if (action == "sell" or action == "cancelBuy"):
                if (price >= DCHigh):  # and ATR <= 0.0007 and ATR >= 0.0005):
                    # if (price < SMA - STDEV):
                    # DChit += 1
                    # if (DChit == 5):
                    #     DChit = 0
                    profitTarget = 0.0001
                    lossTarget = 0.0001
                    #     print(STDEV)
                    openBuyPrice = round(price + 0.00001, roundDec)  # round(candleOpen - 1.5 * ATR, 2)

                    # ATRBuy = ATR
                    # print("price", price)
                    # print("ATR", ATR)
                    # print("SMA", SMA)
                    # print("candleClosePrice", candleClosePrice)
                    # print("candleLowPrice", candleLowPrice)
                    # print("DCLow", DCLow)
                    # # print("SMAHigh", SMAHigh)
                    # print("openBuyPrice", openBuyPrice)

                    # profitWanted = profitTarget * 2 ** inRow !!!
                    # equityAsset = profitWanted / profitTarget !!!
                    # betSize = (0.52*2-1)/(2-1)

                    profitPrice = round(openBuyPrice + profitTarget, roundDec)
                    lossPrice = round(openBuyPrice - lossTarget, roundDec)

                    profitFee = openBuyPrice * takerFee + profitPrice * makerFee
                    lossFee = openBuyPrice * takerFee + lossPrice * takerFee

                    potentialRisk = 1 - (lossPrice - lossFee) / openBuyPrice
                    print("potentialRisk", potentialRisk)
                    riskWanted = (0.466 * 1.9 - 1) / (1.9 - 1)
                    print("riskWanted", riskWanted)
                    equityAsset = (equityCurrency * riskWanted) / openBuyPrice

                    potentialProfit = equityAsset * (profitTarget - profitFee)
                    potentialLoss = equityAsset * (lossTarget + lossFee)

                    #
                    # assetTradeList.append(equityAsset)
                    # currencyTradeList.append(equityAsset * price)
                    # feeList.append(lossFee * equityAsset)
                    action = "closeBuy"

        # if (action == "openBuy"):
        #     if (price < openBuyPrice):
        #         action = "closeBuy"
        #         # print("closeBuy", price)
        #         # print("Asset bought:", equityAsset)
        #         # print("Equity Fiat:", equityCurrency)
        #
        #     elif (price > DCLow):  # or ATR > ATRFilterHigh):  # and ATR > ATRFilterHigh and ATR < ATRFilterLow):
        #         action = "cancelBuy"
        #         canceledTrades += 1
        #         # print("Canceled", price)

        if (action == "closeBuy"):
            if (price > profitPrice):
                action = "sell"
                profitableTrades += 1
                equityCurrency += potentialProfit
                # inRow += 1
                # if (inRow == geomP):
                #     inRow = 0
                #     hit += 1
                # for key, value in ATRDictWin.items():
                #     startRange = str(key).split(":")[0]
                #     endRange = str(key).split(":")[1]
                #     if (ATRBuy >= float(startRange) and ATRBuy <= float(endRange)):
                #         ATRDictWin[key] += 1

            elif (price < lossPrice):
                action = "sell"
                loosingTrades += 1
                equityCurrency -= potentialLoss
                # inRow = 0
                # for key, value in ATRDictLoss.items():
                #     startRange = str(key).split(":")[0]
                #     endRange = str(key).split(":")[1]
                #     if (ATRBuy >= float(startRange) and ATRBuy <= float(endRange)):
                #         ATRDictLoss[key] += 1

# compareList = []
# print(len(listQC))
# print(len(results))
# cheklist1 = []
# cheklist2 = []
# for i in range(0, len(results)):
#     cheklist1.append(round(results[i][0] / dcmTS))
# for i in range(0, len(listQC)):
#     cheklist2.append(listQC[i][0])
#
# checklist3  = (list(set(cheklist1).symmetric_difference(set(cheklist2))))
# checklist3.sort()
# for i in range(0, len(checklist3)):
#     print(checklist3[i])
# if (round(results[i][0] / dcmTS) != listQC[i][0]):
#     print(round(results[i][0] / dcmTS), listQC[i][0])

# print(candleList[j])
# while index in range(0, len(results) - 1):
#     ts = round(int(results[index][0]) / dcmTS)
#     price = (float(results[index][priceIndex]))
#
#     if ((ts >= candleOpen) and (ts < candleClose)):
#         candlePricesList.append(price)
#     elif (ts >= candleClose):
#         totalCandlesCount += 1
#         if (len(candlePricesList) > 0):
#
#     else:
#         index += -1
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

# for key, value in ATRDict.items():
#     startRange = str(key).split(":")[0]
#     endRange = str(key).split(":")[1]
#     if (ATR > float(startRange) and ATR < float(endRange)):
#         ATRDict[key] += volume
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

# print("Loss", price)

# feeList = openBuyPrice * makerFee + profitPrice * makerFee
# print("candleLow", candleLow)
# index += 1
totalTrades = profitableTrades + loosingTrades
# print("Bad trades:", badTrades / (totalTrades + badTrades) * 100, "%")
# print("exchange", exchange)
print("Canceled trades:", canceledTrades)
print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
print("Total trades:", totalTrades)
print("Final equity Currency:", equityCurrency)
# print("Hits:", hit)
# print("Fee too high:", feeHigh)
# print("Not Enough Currency", notEnoughCurrency)
# print("Geometric Progression:", geomP)
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
# print("ATR WIN")
# for key, value in ATRDictWin.items():
#     print(key + "-" + str(round((value / profitableTrades) * 100)) + "%")
# print("ATR LOSS")
# for key, value in ATRDictLoss.items():
#     print(key + "-" + str(round((value / loosingTrades) * 100)) + "%")
