import sqlite3
import time
import pandas as pd

import sqlite3

equity = 1
buyVolume = 1
sellVolume = 1
candleCount = 0
candleOpenTime = 0
candleOpen = 0
candleCloseTime = 0
candleClose = 0
candleLow = 0
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
canceledTrades = 0
# start: moment("2018-05-07T16:44:00.000"),
# open: 9310,
# high: 9323.45839637,
# low: 9296.9628717,
# close: 9311.97536384,
# vwp: 9303.288674696432,
# volume: 2.05346087,
# trades: 37

candleSize = 60
historySize = 100

profitTarget = 80
lossTarget = 120
ATRFilter = 50

ATRList = []
DCLowList = []
candleOpenList = []
candleCloseList = []
SMA = 0
SMALow = 0
SMAHigh = 0
conn = sqlite3.connect('gdaxEUR.db')
cur = conn.cursor()
cur.execute("SELECT * FROM candles_EUR_BTC WHERE start >? AND start<?", (1432016040, 1542469920))

for row in cur:

    candleHigh = row[3]
    candleLow = row[4]
    candleOpen = row[2]
    candleOpenTime = row[1]
    # firstOpen 1429753320
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
            print("SMA", SMA)
            print("SMAHigh", SMAHigh)
            print("SMALow", SMALow)
            print("candleOpen", candleOpen)
            print("ATR", ATR)

            # print("DCLow", DCLow)
    if (candleCount >= historySize):
        if (action == "sell" or action == "cancelBuy"):
            if (candleOpen > SMA and ATR < ATRFilter):
                action = "buy"
                openBuyPrice = candleOpen
        elif (action == "openBuy"):
            if (candleLow < openBuyPrice):
                action = "buy"
            elif (candleOpen < SMA or ATR > ATRFilter):
                action = "cancelBuy"
                canceledTrades += 1
            # elif (candleLow < openBuyPrice - lossTarget):
            #     action = "sell"
            #     profitableTrades -= 1
            #     profit -= lossTarget

        elif (action == "buy"):
            if (candleHigh > (openBuyPrice + profitTarget)) and (candleLow < (openBuyPrice - lossTarget)):
                action = "sell"
                badTrades += 1
            elif (candleHigh > (openBuyPrice + profitTarget)):
                action = "sell"
                profitableTrades += 1
                profit += profitTarget
            elif (candleLow < (openBuyPrice - lossTarget)):
                action = "sell"
                loosingTrades += 1
                profit -= lossTarget

totalTrades = profitableTrades + loosingTrades
print("Bad trades:", badTrades / (totalTrades + badTrades) * 100, "%")
print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
print("CanceledTrades", canceledTrades)
print("Total trades", totalTrades)
print("Final Profit", profit)
