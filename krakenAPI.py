import requests
import sqlite3
import time

def list_duplicates(seq):
  seen = set()
  seen_add = seen.add
  # adds all elements it doesn't know yet to seen and all other to seen_twice
  seen_twice = set( x for x in seq if x in seen or seen_add(x) )
  # turn the set into a list (as requested)
  return list( seen_twice )
#1510551949536482481
table = "quotes_BTC_LTC"
con = sqlite3.connect("kraken.db")
c = con.cursor()
c.execute("CREATE TABLE IF NOT EXISTS " + table + " (ts integer UNIQUE,volume real,price real)")
#last = 1510551949536482481
last = 0
response = requests.get("https://api.kraken.com/0/public/Trades?pair=XLTCXXBT&since="+str(last))
data = response.json()
tradesList = []
tsList=[]
while last <= 1546031023705390000:
    print(last)
    if (data != []):
        #print(data)
        if(data['error'] !=[]):
            time.sleep(5)
            print(data['error'])
        else:
            for i in range(0, len(data['result']['XLTCXXBT'])):
                ts = int(data['result']['XLTCXXBT'][i][2] * 10000)
                volume = float(data['result']['XLTCXXBT'][i][1])
                price = float(data['result']['XLTCXXBT'][i][0])
                tup = (ts, volume, price)
                tradesList.append(tup)
            try:
                c.executemany("INSERT INTO %s VALUES (?,?,?)" % table, tradesList)
                con.commit()
            except sqlite3.Error as e:
                print(last)
    tradesList.clear()
    response = requests.get("https://api.kraken.com/0/public/Trades?pair=XLTCXXBT&since=" + (data['result']['last']))
    code = response.status_code

    while code != 200:
        response = requests.get("https://api.kraken.com/0/public/Trades?pair=XLTCXXBT&since=" + (data['result']['last']))
        code = response.status_code
        time.sleep(5)

    data = response.json()
    last = int(data['result']['last'])
    time.sleep(1)
