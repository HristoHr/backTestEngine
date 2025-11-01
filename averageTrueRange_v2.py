import sqlite3

conn = sqlite3.connect('coinbase.db')
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_EUR_BTC WHERE timestamp >?", (1483228800,))
results = cur.fetchall()
print("Candle,History,0-100,100-200,200-300,300-400,500-600,600-700,700-800,800-900,900-1000")
for candleSize in [5, 15, 30, 60, 120, 240]:
    for historySize in range(100, 1100, 100):
        candleCount = 0

        candleOpenTime = 0
        candleOpenPrice = 0
        candleCloseTime = 0
        candleClosePrice = 0
        candleLowPrice = 0
        candleHighPrice = 0
        candlePricesList = []
        # candlePricesList.append(candleOpenPrice)
        candleLowList = []
        candleHighList = []

        DCLow = 0
        DCHigh = 0
        ATR = 0

        atrVolume0 = 0
        atrVolume10 = 0
        atrVolume20 = 0
        atrVolume30 = 0
        atrVolume40 = 0
        atrVolume50 = 0
        atrVolume60 = 0
        atrVolume70 = 0
        atrVolume80 = 0
        atrVolume90 = 0
        atrVolume100 = 0

        index = 0

        for row in results:
            if (index > 0):
                ts = int(row[0])
                price = float(row[1])
                volume = float(row[2])

                if (index == 1):
                    candleOpenTime = ts
                    candleOpenPrice = price

                if ((ts >= candleOpenTime) and (ts < candleOpenTime + 60 * candleSize)):
                    candlePricesList.append(price)
                else:
                    candleOpenTime = ts
                    candleOpenPrice = price
                    candleLowPrice = min(candlePricesList)
                    candleHighPrice = max(candlePricesList)

                    candleLowList.append(candleLowPrice)
                    candleHighList.append(candleHighPrice)

                    candleCount += 1
                    candlePricesList.clear()
                    candlePricesList.append(candleOpenPrice)

                    if (candleCount >= historySize):
                        DCLow = sum(candleLowList) / float(historySize)
                        DCHigh = sum(candleHighList) / float(historySize)
                        ATR = DCHigh - DCLow
                        # print("DCLow", DCLow)
                        # print("DCHigh", DCHigh)
                        # print("ATR", ATR)
                        candleLowList.pop(0)
                        candleHighList.pop(0)

                if (ATR > 0 and ATR <= 100):
                    atrVolume0 += volume
                elif (ATR > 100 and ATR <= 200):
                    atrVolume10 += volume
                elif (ATR > 200 and ATR <= 300):
                    atrVolume20 += volume
                elif (ATR > 300 and ATR <= 400):
                    atrVolume30 += volume
                elif (ATR > 400 and ATR <= 500):
                    atrVolume40 += volume
                elif (ATR > 500 and ATR <= 600):
                    atrVolume50 += volume
                elif (ATR > 600 and ATR <= 700):
                    atrVolume60 += volume
                elif (ATR > 700 and ATR <= 800):
                    atrVolume70 += volume
                elif (ATR > 800 and ATR <= 900):
                    atrVolume80 += volume
                elif (ATR > 900 and ATR <= 1000):
                    atrVolume90 += volume

            index += 1

        # print("Candle, History,0-100,100-200,200-300,300-400,500-600,600-700,700-800,800-900,900-1000")
        print(candleSize, historySize,
              round(atrVolume0 / 1000),
              round(atrVolume10 / 1000),
              round(atrVolume20 / 1000),
              round(atrVolume30 / 1000),
              round(atrVolume40 / 1000),
              round(atrVolume50 / 1000),
              round(atrVolume60 / 1000),
              round(atrVolume70 / 1000),
              round(atrVolume80 / 1000),
              round(atrVolume90 / 1000),
              sep=",")
