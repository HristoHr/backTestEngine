import time
import pandas as pd
import sqlite3
import multiprocessing
import pprint
import itertools

start = time.time()

conn = sqlite3.connect('coinbase.db')
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_EUR_BTC WHERE timestamp >?", (1514764800,))
results = cur.fetchall()


# atrVolume0 = 0
# atrVolume10 = 0
# atrVolume20 = 0
# atrVolume30 = 0
# atrVolume40 = 0
# atrVolume50 = 0
# atrVolume60 = 0
# atrVolume70 = 0
# atrVolume80 = 0
# atrVolume90 = 0
# atrVolume100 = 0
# with open("Output1.txt", "w") as texFile:
#     print("History,Candle,ATR,Target,Canceled,Loosing,Profitable,Total,Equity,Profit,Profit After Fees")
#     print("History,Candle,ATR,Target,Canceled,Loosing,Profitable,Total,Equity,Profit,Profit After Fees",
#           file=texFile)
#


def backTest(params):
    historySize = params[0]
    candleSize = params[1]
    target = params[2]
    # for historySize in [25, 500, 25]:
    # for candleSize in [5, 15, 30, 60, 120, 240]:
    # for target in [50, 100, 200, 250, 300]:
    # for ATRFilter in [50, 300, 25]:
    profit = 0
    profitAfterFees = 0
    equityFiat = 1000
    profitTarget = target
    lossTarget = target
    candleCount = 0
    candleOpenTime = 0
    candleOpenPrice = 0
    candleCloseTime = 0
    candleClosePrice = 0
    candleLowPrice = 0
    candleHighPrice = 0
    candlePricesList = []
    candleLowList = []
    candleOpenList = []
    candleHighList = []
    DCLow = 0
    DCHigh = 0
    ATR = 0
    SMA = 0
    action = "sell"
    openBuyPrice = 0
    closeBuyPrice = 0
    loosingTrades = 0
    profitableTrades = 0
    cancelBuy = 0
    closeBuy = 0
    makerFee = 0
    takerFee = 0.003
    slippage = 3
    makerMargin = 0.5
    lossPrice = 0
    profitPrice = 0
    equityBTC = 0
    index = 0
    for row in results:
        if (index > 0):
            ts = int(row[0])
            price = float(row[1])
            volume = float(row[2])

            if (index == 1):
                candleOpenTime = ts
                candleOpenPrice = price
                # print(time.strftime("%d %b %Y %H:%M:%S", time.localtime(candleOpenTime)))
                # print(candleOpenPrice)

            if ((ts >= candleOpenTime) and (ts < candleOpenTime + 60 * candleSize)):
                candlePricesList.append(price)
            else:
                candleOpenTime = ts
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
                    DCLow = sum(candleLowList) / float(historySize)
                    DCHigh = sum(candleHighList) / float(historySize)
                    SMA = sum(candleOpenList) / float(historySize)
                    ATR = DCHigh - DCLow
                    # print("Date:", time.strftime("%d %b %Y %H:%M:%S", time.localtime(ts)))
                    # print("SMA", SMA)
                    # print("price", price)
                    # print("ATR", ATR)
                    # print("DCLow", DCLow)
                    candleLowList.pop(0)
                    candleHighList.pop(0)
                    candleOpenList.pop(0)

            if (action == "sell" or action == "cancelBuy"):
                if (price > SMA and ATR < 0.05 * price and SMA > 0 and ATR > 0):  # and  ATR <= 20):
                    action = "openBuy"
                    openBuyPrice = price - makerMargin
                    equityBTC = equityFiat / openBuyPrice
                    profitPrice = price + profitTarget
                    lossPrice = price - lossTarget
                    # print("Open Buy at:", time.strftime("%d %b %Y %H:%M:%S", time.localtime(ts)))

            elif (action == "openBuy"):
                if (price < openBuyPrice):
                    action = "closeBuy"
                    closeBuy += 1
                    # print("Close Buy at:", price)
                else:
                    # if(price>openBuyPrice+profitTarget):
                    if (price < SMA or ATR > 0.05 * price):
                        action = "cancelBuy"
                        cancelBuy += 1
                        # print("Cancel Buy")
            elif (action == "closeBuy"):
                if (price > profitPrice):
                    action = "sell"
                    profitableTrades += 1
                    profitFee = openBuyPrice * makerFee + profitPrice * makerFee
                    equityFiat += (profitTarget + profitFee) * equityBTC
                    profit += profitTarget
                    profitAfterFees += profitTarget + profitFee
                    # print("Profit at:", price)
                elif (price < lossPrice):
                    action = "sell"
                    loosingTrades += 1
                    lossFee = openBuyPrice * makerFee + lossPrice * takerFee
                    equityFiat -= (lossTarget + lossFee + slippage) * equityBTC
                    profit -= lossTarget
                    profitAfterFees -= lossTarget + lossFee + slippage
                    # print("Loss at:", price)

        index += 1
    totalTrades = profitableTrades + loosingTrades
    loosingPer100 = round((loosingTrades / totalTrades) * 100, 2)
    profitablePer100 = round((profitableTrades / totalTrades) * 100, 2)
    # ("History,Candle,ATR,Target,Canceled,Loosing,Profitable,Total,Equity,Profit,Profit After Fees")

    # print(historySize, candleSize, target, '5%', cancelBuy, loosingPer100, profitablePer100,
    #       totalTrades, round(equityFiat), profit, round(profitAfterFees), sep=",", file=texFile)
    print(historySize, candleSize, ATR, target, cancelBuy, loosingPer100, profitablePer100,
          totalTrades, round(equityFiat), profit, round(profitAfterFees))


processes = 5
pool = multiprocessing.Pool(processes=processes)

historySize = range(400, 1100, 100)
candleSize = [60, 120]
target = range(100, 300, 100)
paramlist = list(itertools.product(historySize, candleSize, target))

pool.map(backTest, paramlist)
end = time.time()

print("processes", processes, "Time to complete: ", (end - start))
# print("candleSize", candleSize, "target", target, "ATRFilter", ATRFilter)
# print("Canceled Trades:", cancelBuy)
# print("Loosing Trades:", (loosingTrades / totalTrades) * 100, "%")
# print("Profitable Trades:", (profitableTrades / totalTrades) * 100, "%")
# print("Total Trades:", totalTrades)
# print("Final Equity:", equityFiat)
# print("Final Profit:", profit)
# print("Final Profit After Fees:", profitAfterFees)
# print("Candle,Target,ATR Filter,Canceled,Loosing,Profitable,Total,Equity,Profit,Profit After Fees")
# print("ATR 0-10 volume", atrVolume0)
# print("ATR 10-20 volume", atrVolume10)
# print("ATR 20-30 volume", atrVolume20)
# print("ATR 30-40 volume", atrVolume30)
# print("ATR 40-50 volume", atrVolume40)
# print("ATR 50-60 volume", atrVolume50)
# print("ATR 60-70 volume", atrVolume60)
# print("ATR 70-80 volume", atrVolume70)
# print("ATR 80-90 volume", atrVolume80)
# print("ATR 90-100 volume", atrVolume90)
