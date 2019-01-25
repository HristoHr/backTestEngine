import sqlite3
import time
import pandas as pd

import sqlite3

equityBTC = 1
equityAlt = 0
buyVolume = 1
sellVolume = 1
candleCount = 0
candleOpenTime = 0
candleOpen = 0
candleCloseTime = 0
candleClose = 0
candleLow = 0
canceledTrades = 0
candleHigh = 0
candlePricesList = []
# candlePricesList.append(candleOpenPrice)
candleLowList = []
candleHighList = []
ATR = 0
action = "sell"
openBuyPrice = 0
loosingTrades = 0
profitableTrades = 0
badTrades = 0
profit = 0
geomProg = 1
profitRow = 0
candleHighestList = []
candleLowestList = []
# start: moment("2018-05-07T16:44:00.000"),
# open: 9310,
# high: 9323.45839637,
# low: 9296.9628717,
# close: 9311.97536384,
# vwp: 9303.288674696432,
# volume: 2.05346087,
# trades: 37

candleSize = 15
historySize = 14

profitTarget = 0.0025
lossTarget = 0.0025
ATRFilterLow = 0.00005
ATRFilterHigh = 0.0004
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
makerFee = 0.0/100
takerFee = 0.03/100
geomP = 0
inRow = 0
#
# for i in range(100, 2500, 100):
#     key = str((i - 100) / 1000000) + ":" + str(i / 1000000)
#     ATRDict[key] = 0

conn = sqlite3.connect('bitfinexBTC.db')
cur = conn.cursor()
cur.execute("SELECT * FROM candles_BTC_LTC")  # WHERE start >? AND start<?", (1517443200, 1542469920))

for row in cur:

    candleHigh = row[3]
    candleLow = row[4]
    candleOpen = row[2]
    candleOpenTime = row[1]
    candleVolume = row[7]
    print(candleOpenTime)
    if (len(candleHighList) < candleSize):
        candleHighList.append(candleHigh)
        candleLowList.append(candleLow)
    else:
        candleHighest = max(candleHighList)
        candleLowest = min(candleLowList)

        candleHighList = []
        candleLowList = []

        candleHighestList.append(candleHighest)
        candleLowestList.append(candleLowest)
        candleOpenList.append(candleOpen)
        candleCount += 1

        if (len(candleOpenList) >= historySize):
            SMA = sum(candleOpenList) / len(candleOpenList)
            SMAHigh = sum(candleHighestList) / len(candleHighestList)
            SMALow = sum(candleLowestList) / len(candleLowestList)
            ATR = SMAHigh - SMALow

            candleOpenList.pop(0)
            candleHighestList.pop(0)
            candleLowestList.pop(0)
            # print("Date:", time.strftime("%d %b %Y %H:%M:%S", time.localtime(candleOpenTime)))
            # print("SMA", SMA)
            # print("SMAHigh", SMAHigh)
            # print("SMALow", SMALow)
            # print("candleOpen", candleOpen)
            # print("ATR", ATR)
            # print("DCLow", DCLow)

    if (candleCount >= historySize):
        # for key, value in ATRDict.items():
        #     startRange = str(key).split(":")[0]
        #     endRange = str(key).split(":")[1]
        #     if (ATR > float(startRange) and ATR < float(endRange)):
        #         ATRDict[key] += candleVolume
        profitTarget = 1 * ATR
        lossTarget = 1.5 * ATR

        if (action == "sell" or action == "cancelBuy"):
            if (candleOpen < SMA and ATR < ATRFilterHigh and ATR > ATRFilterLow):
                openBuyPrice = candleOpen - 1.5 * ATR #round(candleOpen - 1.5 * ATR, 2)
                equityAlt = ((equityBTC / geomP) * 2 ** inRow) / openBuyPrice
                # profitPrice = openBuyPrice + profitTarget
                lossPrice = openBuyPrice - lossTarget
                # profitFee = openBuyPrice * makerFee + profitPrice * makerFee
                lossFee = openBuyPrice * makerFee + lossPrice * takerFee
                potentialProfit = equityAlt * profitTarget
                if(potentialProfit > lossFee):
                    action = "openBuy"

            # print("openBuyPrice", openBuyPrice)
        if (action == "openBuy"):
            # if(candleLow < openBuyPrice and candleOpen > SMALow):
            #     action = "cancelBuy"
            #   canceledTrades += 1
            if (candleLow < openBuyPrice):
                action = "closeBuy"
            elif (candleOpen > SMAHigh):  # and ATR > ATRFilterHigh and ATR < ATRFilterLow):
                action = "cancelBuy"
                canceledTrades += 1
        if (action == "closeBuy"):
            if (candleHigh > (openBuyPrice + profitTarget)) and (candleLow < (openBuyPrice - lossTarget)):
                action = "sell"
                badTrades += 1
            elif (candleHigh > (openBuyPrice + profitTarget)):
                action = "sell"
                profitableTrades += 1
                profit += profitTarget
                # print("candleHigh", candleHigh)
            elif (candleLow < (openBuyPrice - lossTarget)):
                action = "sell"
                loosingTrades += 1
                profit -= lossTarget
                #feeList = openBuyPrice * makerFee + profitPrice * makerFee
                # print("candleLow", candleLow)
totalTrades = profitableTrades + loosingTrades
print("Bad trades:", badTrades / (totalTrades + badTrades) * 100, "%")
print("Canceled trades:", canceledTrades)
print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
print("Total trades", totalTrades)
print("Final Profit", profit)
# for key, value in ATRDict.items():
#    print(key + "-" + str(round(value / 1000)))
