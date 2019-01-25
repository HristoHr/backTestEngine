import time
import pandas as pd
import sqlite3

start = time.time()

conn = sqlite3.connect('coinbase.db')
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_EUR_BTC WHERE timestamp >? AND timestamp<?", (1432016040,1542469920))
results = cur.fetchall()

# mvn package exec:exec -DCsvImport \
#                  -Dbigtable.projectID=alloe-api \
#                                       -Dbigtable.instanceID=analysis-sandbox \
#                                                             -DinputFile="gs://clainmscsv/sampleClainms.csv" \
#                                                                 -DbigtableTableId=claimsTable0
#                                                                         -Dheaders="RowKey,Claim Number,Claim Type,Dependent Number,Out of Area Provider Tax ID Number,Revenue/Procedure,Revenue/Procedure Description,Procedure Code Modifier,Line Number,Diagnosis Code,Diagnosis,Package Number,Physician Name,Physician Street Address 1,Physician Street Address 2,Physician City,Physician State,Physician Zip 5,Claim Received Date,Claim Paid Date,Start Service Date,End Service Date,Line Paid Units,Line Charge Amount,Line Deductible Amount,Line Co-pay Amount,Line Coinsurance Amount,Line Penalty Amount,Line Paid Amount"

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
profit = 0
profitAfterFees = 0
equityFiat = 1000

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
SMALow = 0
SMAHigh = 0
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
makerMargin = 0.05
lossPrice = 0
profitPrice = 0
equityBTC = 0
inRow = 0
geomP = 1
index = 0

candleSize = 60
historySize = 100

profitTarget = 80
lossTarget = 120
ATRFilter = 50

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
                SMALow = sum(candleLowList) / float(historySize)
                SMAHigh = sum(candleHighList) / float(historySize)
                SMA = sum(candleOpenList) / float(historySize)
                ATR = SMAHigh - SMALow
                # print("Date:", time.strftime("%d %b %Y %H:%M:%S", time.localtime(ts)))
                print("SMA", SMA)
                print("SMAHigh", SMAHigh)
                print("SMALow", SMALow)
                print("ATR", ATR)
                print("ts", ts)
                candleLowList.pop(0)
                candleHighList.pop(0)
                candleOpenList.pop(0)

        if (candleCount >= historySize):
            if (action == "sell" or action == "cancelBuy"):
                if (price > SMA + 1 and ATR < ATRFilter):
                    action = "openBuy"
                    openBuyPrice = round(price - makerMargin, 2)
                    equityBTC = ((equityFiat / geomP) * 2 ** inRow) / openBuyPrice
                    profitPrice = openBuyPrice + profitTarget
                    lossPrice = openBuyPrice - lossTarget
                    print("Open Buy at:", openBuyPrice)

            elif (action == "openBuy"):
                if (price < openBuyPrice):
                    action = "closeBuy"
                    closeBuy += 1
                    print("Close Buy at:", price)
                else:
                    # if(price>openBuyPrice+profitTarget):
                    if (price < SMA or ATR > ATRFilter):
                        action = "cancelBuy"
                        cancelBuy += 1
                        print("Cancel Buy")
            elif (action == "closeBuy"):
                if (price > profitPrice):
                    action = "sell"
                    profitableTrades += 1
                    profitFee = openBuyPrice * makerFee + profitPrice * makerFee
                    equityFiat += (profitTarget - profitFee) * equityBTC
                    profit += profitTarget
                    profitAfterFees += (profitTarget - profitFee)
                    inRow += 1
                    if (inRow == geomP):
                        inRow = 0
                    print("Profit at:", price)
                elif (price < lossPrice):
                    action = "sell"
                    loosingTrades += 1
                    slippage = lossPrice - price
                    lossFee = openBuyPrice * makerFee + lossPrice * takerFee
                    equityFiat -= (lossTarget + lossFee + slippage) * equityBTC
                    profit -= lossTarget
                    profitAfterFees -= (lossTarget + lossFee)
                    inRow = 0
                    print("Loss at:", price)

    index += 1
totalTrades = profitableTrades + loosingTrades
loosingPer100 = round((loosingTrades / totalTrades) * 100, 2)
profitablePer100 = round((profitableTrades / totalTrades) * 100, 2)
# ("History,Candle,ATR,Target,Canceled,Loosing,Profitable,Total,Equity,Profit,Profit After Fees")
print(historySize, candleSize, ATRFilter, profitTarget, lossTarget, cancelBuy, loosingPer100, profitablePer100,
      totalTrades, round(equityFiat), profit, round(profitAfterFees), sep=",")
