import sqlite3
import time
import pandas as pd
# import pandas_datareader as datareader
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import sqlite3

# def zoom_factory(ax,base_scale = 2.):
#     def zoom_fun(event):
#         # get the current x and y limits
#         cur_xlim = ax.get_xlim()
#         cur_ylim = ax.get_ylim()
#         cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
#         cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
#         xdata = event.xdata # get event x location
#         ydata = event.ydata # get event y location
#         if event.button == 'up':
#             # deal with zoom in
#             scale_factor = 1/base_scale
#         elif event.button == 'down':
#             # deal with zoom out
#             scale_factor = base_scale
#         else:
#             # deal with something that should never happen
#             scale_factor = 1
#             print(event.button)
#         # set new limits
#         ax.set_xlim([xdata - cur_xrange*scale_factor,
#                      xdata + cur_xrange*scale_factor])
#         ax.set_ylim([ydata - cur_yrange*scale_factor,
#                      ydata + cur_yrange*scale_factor])
#         plt.draw() # force re-draw
#
#     fig = ax.get_figure() # get the figure of interest
#     # attach the call back
#     fig.canvas.mpl_connect('scroll_event',zoom_fun)
#
#     #return the function
#     return zoom_fun

equityCurrency = 500000
equityAsset = 0
createdCandlesCount = 0
candleOpenTime = 0
candleOpenTs = 0
candleCloseTime = 0
candleCloseTs = 0
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
candleSize = 60
historySize = 24
potentialLoss = 0
potentialProfit = 0
profitWantedDefault = 0.010
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

conn = sqlite3.connect('bitfinex.db')
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_BTC_LTC")  # WHERE ts >?", (1479874700,))

SMAList = []
_candleTsList = []
_candleOpenList = []
_candleHighList = []
_candleLowList = []
_candleCloseList = []
_buyList = []
_sellProfitList = []
_sellLossList = []
ts = 0
price = 0

index = 0
for row in cur:
    index += 1
    if (index > 1):
        ts = round(int(row[0]))
        price = float(row[2])
        volume = float(row[1])
        print(ts)
        if (index == 2):
            start = round((ts) / 100) * 100 + 60 * candleSize
            for i in range(start, 1546162730000, 60 * candleSize):
                candleList.append(i)
            continue
            # print(i)
            # candleOpenTime = ts
            # candleOpenPrice = volume
            # totalCandles = len(candleList)
            # print(time.strftime("%d %b %Y %H:%M:%S", time.localtime(candleOpenTime)))
            # print(candleOpenPrice)
        candleOpenTs = candleList[totalCandlesCount]
        candleCloseTs = candleList[totalCandlesCount + 1]
        # print("candleOpen", candleOpen)
        # print("candleClose", candleClose)
        # print(ts)
        if ((ts >= candleOpenTs) and (ts < candleCloseTs)):
            candlePricesList.append(price)
        elif (ts >= candleCloseTs):
            totalCandlesCount += 1
            if (len(candlePricesList) > 0):
                candleOpenPrice = candlePricesList[0]
                candleHighPrice = max(candlePricesList)
                candleLowPrice = min(candlePricesList)
                candleClosePrice = candlePricesList[-1]

                candleOpenList.append(candleOpenPrice)
                candleHighList.append(candleHighPrice)
                candleLowList.append(candleLowPrice)
                candleCloseList.append(candleClosePrice)
                createdCandlesCount += 1
                candlePricesList.clear()
                # candlePricesList.append(candleClosePrice)
                if (createdCandlesCount >= historySize):
                    _candleTsList.append(candleOpenTs)
                    _candleOpenList.append(candleOpenPrice)
                    _candleHighList.append(candleHighPrice)
                    _candleLowList.append(candleLowPrice)
                    _candleCloseList.append(candleClosePrice)

                    SMALow = round(sum(candleLowList) / len(candleLowList), 6)
                    SMAHigh = round(sum(candleHighList) / len(candleHighList), 6)
                    SMA = round(sum(candleCloseList) / len(candleCloseList), 6)
                    ATR = round(SMAHigh - SMALow, 6)

                    DCLow = round(min(candleLowList), 6)
                    DCHigh = round(max(candleHighList), 6)
                    DCMid = round(DCHigh - DCLow, 6)

                    SMAList.append(SMALow)

                    candleLowList.pop(0)
                    candleHighList.pop(0)
                    candleOpenList.pop(0)
                    candleCloseList.pop(0)
            else:
                badTrades += 1

        # if action == "sell" or action == "cancelBuy":
        #     profitTarget = ATR
        #     lossTarget = ATR
        #
        #     openBuyPrice = round((price - 0.000001), 6)  # round(candleOpen - 1.5 * ATR, 2)
        #     # print("price", price)
        #     # print("ATR", ATR)
        #     # print("SMA", SMA)
        #     # print("candleClosePrice", candleClosePrice)
        #     # print("candleLowPrice", candleLowPrice)
        #     # print("SMALow", SMALow)
        #     # # print("SMAHigh", SMAHigh)
        #     # print("openBuyPrice", openBuyPrice)
        #     profitWanted = profitWantedDefault * 2 ** inRow
        #     equityAsset = profitWanted / profitTarget
        #
        #     profitPrice = openBuyPrice + profitTarget
        #     lossPrice = openBuyPrice - lossTarget
        #
        #     profitFee = openBuyPrice * makerFee + profitPrice * makerFee
        #     lossFee = openBuyPrice * makerFee + lossPrice * takerFee
        #
        #     potentialProfit = equityAsset * (profitTarget - profitFee)
        #     potentialLoss = equityAsset * (lossTarget + lossFee)
        #
        #     assetTradeList.append(equityAsset)
        #     currencyTradeList.append(equityAsset * price)
        #     feeList.append(lossFee * equityAsset)
        #     action = "closeBuy"
        #     _buyList.append((ts, price))
        #     # if (equityCurrency / openBuyPrice >= equityAsset):
        #     #     # potentialRatio = potentialProfit / potentialLoss
        #     #     # wantedRatio = profitWantedDefault / lossWantedDefault
        #     #     # if (potentialRatio >= 8 / 13):
        #     #     #     feeHigh += 1
        #     #     # else:
        #     #
        #     #
        #     #     # print("Open Buy at:", openBuyPrice)
        #     #     # print("Wanted Profit:", profitWanted)
        #     #     continue
        #     # else:
        #     #     notEnoughCurrency += 1
        #     #     print("Not Enough $$$")
        #     #     continue
        #     # print("Not Enough Asset !!!")
        #     # print("openBuyPrice", openBuyPrice)
        # if (action == "openBuy"):
        #     if (price < openBuyPrice):
        #         action = "closeBuy"
        #         # print("closeBuy", price)
        #         # print("Asset bought:", equityAsset)
        #         # print("Equity Fiat:", equityCurrency)
        #         continue
        #
        #     elif (price > profitPrice):  # or ATR > ATRFilterHigh):  # and ATR > ATRFilterHigh and ATR < ATRFilterLow):
        #         action = "cancelBuy"
        #         canceledTrades += 1
        #         # print("Canceled", price)
        #         continue
        #
        # if (action == "closeBuy"):
        #     if (price > profitPrice):
        #         _sellProfitList.append((ts, price))
        #         action = "sell"
        #         profitableTrades += 1
        #         equityCurrency += potentialProfit
        #         inRow += 1
        #         if (inRow == geomP):
        #             inRow = 0
        #             hit += 1
        #         # print("Profit", price)
        #         continue
        #     elif (price < lossPrice):
        #         _sellLossList.append((ts, price))
        #         action = "sell"
        #         loosingTrades += 1
        #         equityCurrency -= potentialLoss
        #         inRow = 0
        #         # print("Loss", price)
        #         continue
        #     # feeList = openBuyPrice * makerFee + profitPrice * makerFee
        #     # print("candleLow", candleLow)
        # totalTrades = profitableTrades + loosingTrades
        # # print("Bad trades:", badTrades / (totalTrades + badTrades) * 100, "%")
        # print("Canceled trades:", canceledTrades)
        # print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
        # print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
        # print("Total trades:", totalTrades)
        # print("Final equity Currency:", equityCurrency)
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
        # print("Missing Candles", missingCandlesCount)
        # print("Created Candles", createdCandlesCount)
        # print("Total Candles", totalCandlesCount)
print("Bad Trades", badTrades)

quotes = [tuple([_candleTsList[i],
                 _candleOpenList[i],
                 _candleHighList[i],
                 _candleLowList[i],
                 _candleCloseList[i]]) for i in range(len(_candleTsList))]  # _1

fig,ax = plt.subplots()
scale = 1.5
# fig = zoom_factory(ax,base_scale = scale)
candlestick_ohlc(ax, quotes, width=6)

# sma = [[kurse_c[i] * 0.8] for i in range(len(_candleTsList))]
data = pd.DataFrame(SMAList, index=_candleTsList, columns=["sma"])  # _2
data = data.astype(float)
data["sma"].plot(ax=ax)

# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# ax.grid(True)

plt.show()
