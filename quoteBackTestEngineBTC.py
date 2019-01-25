import sqlite3
import time
import pandas as pd

import sqlite3

equityBTC = 5
equityAlt = 0
candleCount = 0
candleOpenTime = 0
candleOpen = 0
candleCloseTime = 0
candleClose = 0
candleLow = 0
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
candleSize = 1
historySize = 5
potentialLoss = 0
potentialProfit = 0
profitWantedDefault = 0.006
lossWantedDefault = 0.006
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
makerFee = 0.0 / 100
takerFee = 0.03 / 100
geomP = 2
inRow = 0
hit = 0
feeHigh = 0
bought = True
lossFee = 0
candleOpenPrice = 0
profitPrice = 0
lossPrice = 0
notEnoughBTC = 0
altTradeList = []
btcTradeList = []
DCHighList = []
DCMidList = []
# for i in range(10, 500, 20):000
#     key = str((i - 10)) + ":" + str(i)
#     ATRDict[key] = 0

conn = sqlite3.connect('gdax_0.1.db')
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_BTC_LTC ORDER BY ts")  # WHERE timestamp >?", (1483318861,))

index = 0
price = 0

DCLow = 0
DCHigh = 0
DCMid = 0
for row in cur:
    index += 1
    if (index > 1):
        ts = int(row[0])
        price = float(row[1])
        volume = float(row[2])
        # print(ts)
        if (index == 2):
            candleOpenTime = ts
            candleCloseTime = candleOpenTime + 60 * candleSize
            candleOpenPrice = price
            # print(time.strftime("%d %b %Y %H:%M:%S", time.localtime(candleOpenTime)))
            # print(candleOpenPrice)
        if ((ts >= candleOpenTime) and (ts < candleCloseTime)):
            candlePricesList.append(price)
        else:
            candleOpenTime = ts
            candleCloseTime = candleOpenTime + 60 * candleSize
            print(time.strftime("%d %b %Y %H:%M:%S", time.localtime(candleOpenTime)))
            candleOpenPrice = price
            candleLowPrice = min(candlePricesList)
            candleHighPrice = max(candlePricesList)

            candleLowList.append(candleLowPrice)
            candleHighList.append(candleHighPrice)
            candleOpenList.append(candleOpenPrice)

            candleCount += 1
            candlePricesList.clear()
            candlePricesList.append(candleOpenPrice)

            if (candleCount >= historySize):
                # if (candleOpenTime >= 1486900260 and candleOpenTime <= 1486909360):
                #     print(ATR)
                SMALow = sum(candleLowList) / len(candleLowList)
                SMAHigh = sum(candleHighList) / len(candleHighList)
                SMA = sum(candleOpenList) / len(candleOpenList)
                ATR = SMAHigh - SMALow
                DCLowList.append(min(candleLowList))
                DCHighList.append(max(candleHighList))
                # DCMidList.append(DCHigh - DCLow)
                DCLow = DCLowList[-1]
                DCHigh = DCHighList[-1]
                # print("DCLow", DCLow)
                # DCMid =  DCMidList.pop()
                # DCLow = min(candleLowList)
                # DCHigh = max(candleHighList)
                # DCMid = DCHigh - DCLow
                candleLowList.pop(0)
                candleHighList.pop(0)
                candleOpenList.pop(0)

    if (ATR == 0):
        # action = "cancelBuy"
        continue
    else:
        # if (candleCount >= historySize):
        #     # for key, value in ATRDict.items():
        #     #     startRange = str(key).split(":")[0]
        #     #     endRange = str(key).split(":")[1]
        #     #     if (ATR > float(startRange) and ATR < float(endRange)):
        #     #         ATRDict[key] += volume
        #     print(ATR)

        if (action == "sell" or action == "cancelBuy") and (
                candleOpenPrice < SMALow and candleOpenPrice > DCLow):  # and ATR < ATRFilterHigh and ATR > ATRFilterLow):

            profitTarget = profitWantedDefault
            lossTarget = profitTarget  # SMAHigh-SMA
            # if(profitTarget <= 0 or lossTarget <= 0):
            #     continue
            openBuyPrice = price  # round(candleOpen - 1.5 * ATR, 2)
            # print("price", price)
            # print("ATR", ATR)
            # print("SMA", SMA)

            # print("SMAHigh", SMAHigh)
            # print("openBuyPrice", openBuyPrice)
            profitWanted = profitWantedDefault * 2 ** inRow
            equityAlt = profitWanted / profitTarget

            profitPrice = openBuyPrice + profitTarget
            lossPrice = openBuyPrice - lossTarget

            profitFee = openBuyPrice * takerFee + profitPrice * makerFee
            lossFee = openBuyPrice * makerFee + lossPrice * takerFee

            potentialProfit = equityAlt * (profitTarget - profitFee)
            potentialLoss = equityAlt * (lossTarget + lossFee)

            altTradeList.append(equityAlt)
            btcTradeList.append(equityAlt * price)
            feeList.append(lossFee * equityAlt)
            action = "closeBuy"
            # print(ts)
            # if (equityBTC / openBuyPrice >= equityAlt):
            #     # potentialRatio = potentialProfit / potentialLoss
            #     # wantedRatio = profitWantedDefault / lossWantedDefault
            #     # if (potentialRatio >= 8 / 13):
            #     #     feeHigh += 1
            #     # else:
            #
            #     action = "closeBuy"
            #     # print("Open Buy at:", openBuyPrice)
            #     # print("Wanted Profit:", profitWanted)
            #     continue
            # else:
            #     notEnoughBTC += 1
            #     print("Not Enough $$$")
            #     continue
            # print("Not Enough BTC !!!")
        # print("openBuyPrice", openBuyPrice)
        if (action == "openBuy"):
            if (price < openBuyPrice):
                action = "closeBuy"
                # print("Alt bought:", equityAlt)
                # print("Equity BTC:", equityBTC)
                continue

            elif (price > profitPrice):  # or ATR > ATRFilterHigh):  # and ATR > ATRFilterHigh and ATR < ATRFilterLow):
                action = "cancelBuy"
                canceledTrades += 1
                # print("Canceled")
                continue

        if (action == "closeBuy"):
            if (price > profitPrice):
                action = "sell"
                profitableTrades += 1
                equityBTC += potentialProfit
                inRow += 1
                if (inRow == geomP):
                    inRow = 0
                    hit += 1
                # print("Profit")
                continue
            elif (price < lossPrice):
                action = "sell"
                loosingTrades += 1
                equityBTC -= potentialLoss
                inRow = 0
                # print("Loss")
                continue
            # feeList = openBuyPrice * makerFee + profitPrice * makerFee
            # print("candleLow", candleLow)
totalTrades = profitableTrades + loosingTrades
# print("Bad trades:", badTrades / (totalTrades + badTrades) * 100, "%")
print("Canceled trades:", canceledTrades)
print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
print("Total trades:", totalTrades)
print("Final equity BTC:", equityBTC)
print("Hits:", hit)
print("Fee too high:", feeHigh)
print("Not Enough BTC", notEnoughBTC)
print("Geometric Progression:", geomP)
print("Max Alt needed", max(altTradeList))
print("Avr Alt needed", sum(altTradeList) / len(altTradeList))
print("Max BTC needed", max(btcTradeList))
print("Avr BTC needed", sum(btcTradeList) / len(altTradeList))
print("Max Fee", max(feeList))
print("Avr Fee", sum(feeList) / len(feeList))
print(candleCount)
# for key, value in ATRDict.items():
#     print(key + "-" + str(round(value / 1000)))
