import time
import pandas as pd
import sqlite3
conn = sqlite3.connect('coinbase.db')
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_EUR_BTC WHERE timestamp >?", (1429753320,))
results = cur.fetchall()

profit = 0
profitAfterFees = 0
equityFiat = 1000
profitTarget = 80
lossTarget = 100
candleSize = 10
historySize = 120
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
slippage = 0
makerMargin = 0.0
lossPrice = 0
profitPrice = 0
equityBTC = 0
inRow = 0
geomP = 2
index = 0
ATRFilter = 50
for row in results:
    if (index > 0):
        ts = int(row[0])
        price = float(row[1])
        volume = float(row[2])

        if (index == 1):
            candleOpenTime = ts
            candleOpenPrice = volume
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
                # if (candleOpenTime >= 1486900260 and candleOpenTime <= 1486909360):
                #     print(ATR)
                SMALow = sum(candleLowList) / float(historySize)
                SMAHigh = sum(candleHighList) / float(historySize)
                SMA = sum(candleOpenList) / float(historySize)
                ATR = SMAHigh - SMALow
                DCLow = min(candleLowList)
                DCHigh = max(candleHighList)
                DCMid = DCHigh - DCLow
                candleLowList.pop(0)
                candleHighList.pop(0)
                candleOpenList.pop(0)

        if (candleCount >= historySize):
            if (action == "sell" and price > SMA + 1 and ATR < ATRFilter):
                # test = "price >DCMId and ATR < 1% win:loss", profitTarget, " : ", lossTarget
                # test = "nothing", profitTarget, " : ", lossTarget
                action = "buy"
                openBuyPrice = price - makerMargin
                equityBTC = equityFiat / openBuyPrice
                profitPrice = openBuyPrice + profitTarget
                lossPrice = openBuyPrice - lossTarget
                #print("Buy at:", price)
            elif (action == "buy"):
                if (price > profitPrice):
                    action = "sell"
                    profitableTrades += 1
                    profit += profitTarget
                    profitFee = openBuyPrice * takerFee + profitPrice * makerFee
                    profitAfterFees += profitTarget
                    profitAfterFees -= profitFee
                    equityFiat += ((equityBTC / geomP) * 2 ** inRow)*(profitTarget-profitFee)
                    inRow += 1
                    if (inRow == geomP):
                        inRow = 0
                    # profit += (openBuyPrice * profitTarget - openBuyPrice)
                    # equityFiat += (openBuyPrice * profitTarget - openBuyPrice) * equityBTC
                    #print("Profit at:", price)
                elif (price < lossPrice):
                    action = "sell"
                    loosingTrades += 1
                    slippage = lossPrice - price
                    profit -= lossTarget
                    lossFee = openBuyPrice * takerFee + lossPrice * takerFee
                    profitAfterFees -= lossTarget
                    profitAfterFees -= lossFee
                    profitAfterFees -= slippage
                    equityFiat -= (equityBTC / geomP * 2 ** inRow) *(lossTarget+slippage+lossFee)
                    inRow = 0
                    #print("Loss at:", price)
                    # profit -= (openBuyPrice - openBuyPrice * lossTarget) * 1.003
                    # equityFiat -= (openBuyPrice - openBuyPrice * lossTarget) * 1.003 * equityBTC
        # print("Loss at:", price)
    index += 1
totalTrades = profitableTrades + loosingTrades
#print(test)
print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
print("Total trades", totalTrades)
print("Final Profit", profit)
print("Final Profit After Fees", profitAfterFees)
print("Final Equity", equityFiat)
