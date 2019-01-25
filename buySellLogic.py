import csv
import time

equity = 0.1
buyQuantity = 0
sellQuantity = 0
action = ""
sellType = ""
openBuyPrice = 0
openSellPrice = 0
openBelowCurrentPrice = 0
numProfitableTrades = 0
numLoosingTrades = 0
profitTarget = 5
lossTarget = 5
profit = 0
rowIndex = 0
openAboveCurrentPrice = 0.01
margin = 1
takerIndex = 0
takerListPrice = []
takerListQuantity = []
fee = 0.000
slippage = 0.1
with open('coinbaseUSD2mil.csv', encoding="utf8") as csvfile:
    # with open('coinbaseUSD100000.csv') as csvfile:

    readCSV = list(csv.reader(csvfile, delimiter=','))

    for row in readCSV:

        ts = int(row[0])
        price = float(row[1])
        quantity = float(row[2])
        date = time.strftime("%d %b %Y %H:%M:%S", time.localtime(ts))

        # if(rowIndex == 0 or rowIndex==(len(readCSV)-1)):
        #     print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(ts)))
        # if(quantity>100):
        #      print(quantity)

        rowIndex += 1

        if (action == "" or action == "sell"):
            action = "openBuy"
            openBuyPrice = price - openBelowCurrentPrice
            buyQuantity = equity
            print("Open buy at: ", openBuyPrice, "Buy Quantity", buyQuantity)

        elif (action == "openBuy"):
            if (price <= openBuyPrice):
                if (quantity >= buyQuantity):
                    action = "buy"
                    sellQuantity = equity
                    buyQuantity = 0
                    print("Close buy")
                else:
                    buyQuantity -= quantity
                    print("Partially fill buy at: ", price, "Buy Quantity Left", buyQuantity)

                    # action = "partialBuy"
        elif (action == "buy"):  # or "partialBuy"):
            if (price <= openBuyPrice - lossTarget):
                action = "sell"
                openSellPrice = openBuyPrice - lossTarget
                loss = (lossTarget + fee * openSellPrice) * equity
                profit -= loss
                numLoosingTrades += 1
                print("Taker Sell at:", openSellPrice, " loss ", loss)
            elif (price >= openBuyPrice + profitTarget - margin):
                action = "openSell"
                openSellPrice = openBuyPrice + profitTarget
                print("Open profitable sell at: ", openBuyPrice, "Sell Quantity", sellQuantity)
        elif (action == "openSell"):
            if (price >= openSellPrice):
                if (quantity >= sellQuantity):
                    action = "sell"
                    profit += profitTarget * equity
                    print("Close Sell")
                    buyQuantity = equity
                    sellQuantity = 0
                    numProfitableTrades += 1
                    print("Close profitable sell at: ", price, "profit", profitTarget)
                else:
                    sellQuantity -= quantity
                    print("Partially fill sell at: ", price, "Sell Quantity Left", sellQuantity)

    # totalTrades = numProfitableTrades + numLoosingTrades
    # print("Loosing trades:", (numLoosingTrades / totalTrades) * 100, "%")
    # print("Profitable trades:", (numProfitableTrades / totalTrades) * 100, "%")
    # print("Total trades", totalTrades)
    # print("Final Profit", profit)
