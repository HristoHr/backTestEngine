import sqlite3
import time
import pandas as pd

import sqlite3

equityFiat = 1000000
equityBTC = 0
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
profitTarget = 0
lossTarget = 0
candleSize = 60
historySize = 48
potentialLoss = 0
potentialProfit = 0
lossWantedDefault = 60
profitWantedDefault = 45
profitWanted = 0

ATRFilterLow = 0.0000
ATRFilterHigh = 100055
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
# for i in range(10, 500, 20):
#     key = str((i - 10)) + ":" + str(i)
#     ATRDict[key] = 0

conn = sqlite3.connect('gdaxEUR.db')
cur = conn.cursor()
cur.execute("SELECT * FROM candles_EUR_BTC ORDER BY start")  # WHERE start >?", (1420160461, ))

for row in cur:

    candleHigh = row[3]
    candleLow = row[4]
    candleOpen = row[2]
    candleOpenTime = row[1]
    candleVolume = row[7]
    # print(candleOpenTime)
    if (len(candleHighList) < candleSize):
        if (len(candleHighList) == 0):
            candleOpenPrice = candleOpen
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
        profitTarget = profitWantedDefault
        lossTarget = lossWantedDefault

        if (action == "sell" or action == "cancelBuy"):
            # if (candleOpen < SMA and ATR < ATRFilterHigh and ATR > ATRFilterLow):
            openBuyPrice = candleOpen - lossTarget  # round(candleOpen - 1.5 * ATR, 2)

            profitWanted = profitWantedDefault * 2 ** inRow
            equityBTC = profitWanted / profitTarget

            profitPrice = openBuyPrice + profitTarget
            lossPrice = openBuyPrice - lossTarget

            profitFee = openBuyPrice * makerFee + profitPrice * makerFee
            lossFee = openBuyPrice * makerFee + lossPrice * takerFee

            potentialProfit = equityBTC * (profitTarget - profitFee)
            potentialLoss = equityBTC * (lossTarget + lossFee)

            if (equityFiat / openBuyPrice >= equityBTC):
                bought = True
                # potentialRatio = potentialProfit / potentialLoss
                # wantedRatio = profitWantedDefault / lossWantedDefault
                # if (potentialRatio < wantedRatio):
                #     feeHigh += 1
                # else:
                action = "openBuy"
                print("Open Buy at:", openBuyPrice)
                print("Wanted Profit:", profitWanted)
                print("BTC bought:", equityBTC)
                print("Equity Fiat:", equityFiat)
            else:
                bought = False

        # print("Not Enough BTC !!!")
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
                print("Canceled")

        if (action == "closeBuy"):
            if (candleHigh > (openBuyPrice + profitTarget)) and (candleLow < (openBuyPrice - lossTarget)):
                action = "sell"
                badTrades += 1
                print("Bad")
            elif (candleHigh > (openBuyPrice + profitTarget)):
                action = "sell"
                if (bought == True):
                    profitableTrades += 1
                    equityFiat += potentialProfit
                inRow += 1
                if (inRow == geomP):
                    inRow = 0
                    hit += 1
                print("Profit")
            elif (candleLow < (openBuyPrice - lossTarget)):
                action = "sell"
                if (bought == True):
                    loosingTrades += 1
                    equityFiat -= potentialLoss

                inRow = 0
                print("Loss")
                # feeList = openBuyPrice * makerFee + profitPrice * makerFee
                # print("candleLow", candleLow)
totalTrades = profitableTrades + loosingTrades
print("Bad trades:", badTrades / (totalTrades + badTrades) * 100, "%")
print("Canceled trades:", canceledTrades)
print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
print("Total trades:", totalTrades)
print("Final equity Fiat:", equityFiat)
print("Hits:", hit)
print("Fee too high:", feeHigh)
print("Geometric Progression:", geomP)
for key, value in ATRDict.items():
    print(key + "-" + str(round(value / 1000)))
