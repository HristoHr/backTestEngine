import sqlite3
import time
import pandas as pd
import numpy as np

action = "sell"
conn = sqlite3.connect("bitmex.db")
cur = conn.cursor()
cur.execute("SELECT * FROM XBTUSD WHERE timestamp >=?", (1514764800,))
results = cur.fetchall()
ordersArr = []  # buyprice,sellprice,action
makerFee = -0.0250 / 100
takerFee = 0.0750 / 100
equityCurrency = 1000000
equityAsset = 0
openBuyPrice = 0
sellOrderAt = 0
buyOrderAt = 0
potentialLoss = 0
potentialProfit = 0
profitableTrades = 0
loosingTrades = 0
for i in range(0, len(results)):
    ts = results[i][0]
    volume = results[i][1]
    price = results[i][2]
    # print("price", price)
    if (len(ordersArr) == 0 and (action == "sell" or action == "closeBuy")):
        openBuyPrice = (price + 0.5)
        print("genesis order:", openBuyPrice)
        equityAsset = (100 / openBuyPrice)
        equityCurrency -= 100
        sellOrderAt = (openBuyPrice + 10)
        buyOrderAt = (openBuyPrice - 10)
        profitFee = openBuyPrice * takerFee + sellOrderAt * makerFee
        potentialProfit = equityAsset * (sellOrderAt - openBuyPrice) - equityAsset * profitFee
        action = "closeBuy"
        ordersArr.append((buyOrderAt, sellOrderAt, potentialProfit))
        # if (action == "openBuy"):
        #     if (price < openBuyPrice):
        #         action = "closeBuy"
        #
    else:
        for j in range(0, len(ordersArr)):

            buyOrderAt = ordersArr[j][0]
            sellOrderAt = ordersArr[j][1]
            potentialProfit = ordersArr[j][2]

            if (price < buyOrderAt):
                equityAsset = (100 / buyOrderAt)
                equityCurrency -= 100
                sellOrderAt = round(openBuyPrice + 10, 2)
                buyOrderAt = round(openBuyPrice - 10, 2)
                profitFee = openBuyPrice * makerFee + sellOrderAt * makerFee
                potentialProfit = equityAsset * (sellOrderAt - openBuyPrice) + equityAsset * profitFee
                ordersArr.append((buyOrderAt, sellOrderAt, potentialProfit))
                print("buyOrderAt", buyOrderAt)

            elif (price > sellOrderAt):
                equityCurrency += potentialProfit + 100
                print("sellOrderAt,", sellOrderAt)
                for z in range(0, len(ordersArr)):
                    ordersArr[z][0] + 10
                ordersArr.pop(j)

    # if (action == "sell" or action == "cancelBuy"):
    #     openBuyPrice = round(price - 0.5, 2)  # round(candleOpen - 1.5 * ATR, 2)
    #     equityAsset = (.1 * equityCurrency / openBuyPrice)

    # profitPrice = round(openBuyPrice * 1.01, 2)
    # lossPrice = round(openBuyPrice * 0.99, 2)

    # profitFee = openBuyPrice * makerFee + sellPrice * makerFee
    # lossFee = openBuyPrice * makerFee + buyPrice * takerFee
    #
    # potentialProfit = equityAsset * (sellPrice - openBuyPrice) + equityAsset * profitFee
    # potentialLoss = equityAsset * (buyPrice - openBuyPrice) + equityAsset * profitFee

    # if (action == "openBuy"):
    #     if (price < openBuyPrice):
    #         action = "closeBuy"
    #
    # if (action == "closeBuy"):
    #     if (price > sellPrice):
    #         action = "sell"
    #         profitableTrades += 1
    #         equityCurrency += potentialProfit
    #     elif (price < buyPrice):
    #         action = "sell"
    #         loosingTrades += 1
    #         equityCurrency -= potentialLoss

totalTrades = profitableTrades + loosingTrades

# print("Canceled trades:", canceledTrades)
print("Loosing trades:", (loosingTrades / totalTrades) * 100, "%")
print("Profitable trades:", (profitableTrades / totalTrades) * 100, "%")
print("Total trades:", totalTrades)
print("Final equity Currency:", equityCurrency)
