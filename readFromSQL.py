import sqlite3
import time
import pandas as pd

import sqlite3

conn = sqlite3.connect('coinbaseUSD')
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_USD_BTC WHERE timestamp >?", (1483228800,))

for row in cur:
    print(row)
