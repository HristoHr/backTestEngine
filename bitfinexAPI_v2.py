import requests
import sqlite3
import time

asset = "ETH"
table = "quotes_BTC_" + asset
con = sqlite3.connect("bitfinex.db")
c = con.cursor()
c.execute("CREATE TABLE IF NOT EXISTS " + table + " (ts integer,volume real,price real)")

urlBase = "https://api.bitfinex.com/v2/trades/t" + asset + "BTC/hist?"
# 1450141590000
startPharam = "1506499767000"
endPharam = 1425754631000
pharams = "limit=1000&start=" + (startPharam) + "&sort=1"
last = 0
response = requests.get(urlBase + pharams)
data = response.json()
tradesList = []
tsList = []
reqCount = 0
error = 0
while startPharam[:4] != "1546":
    print(startPharam)
    if len(data) > 100:
        for i in range(0, len(data)):
            if data[i] != [] and data[i] != 11010:
                # try:
                ts = data[i][1]
                volume = data[i][2]
                price = data[i][3]
                tup = (ts, volume, price)
                tradesList.append(tup)
            # except ValueError as e:
            #     error += 1
            #     print("error", data[i], e, error)
            # except TypeError as e:
            #     error += 1
            #     print("error", data[i], e, error)

        try:
            c.executemany("INSERT INTO %s VALUES (?,?,?)" % table, tradesList)
            con.commit()
            tradesList.clear()
        except sqlite3.Error as e:
            print(e)
            print(tradesList[-1])
            break

        startPharam = str(data[-1][1])
        pharams = "limit=1000&start=" + (startPharam) + "&sort=1"
        response = requests.get(urlBase + pharams)
        data = response.json()
        time.sleep(2)

    else:
        time.sleep(60)
        response = requests.get(urlBase + pharams)
        data = response.json()
        time.sleep(2)
