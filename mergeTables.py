import time
import pandas as pd
import sqlite3

conn1 = sqlite3.connect('bitfinexBTC2015.db')
cur1 = conn1.cursor()
cur1.execute("SELECT * FROM candles_BTC_LTC")
results1 = cur1.fetchall()

conn2 = sqlite3.connect('bitfinexBTC2018.db')
cur2 = conn2.cursor()
cur2.execute("SELECT * FROM candles_BTC_LTC")  # WHERE start >?", (1543207020,))
results2 = cur2.fetchall()

conn3 = sqlite3.connect('bitfinexBTCFULL.db')
cur3 = conn2.cursor()

resultsNoID = []
resultsNoIDClean = []
resultsNoID1 = []
resultsNoID2 = []
# lastID = 1587764
tsListResults = []
for row in results1:
    tup = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    # print(tup)
    tsListResults.append(row[0])
    resultsNoID1.append(tup)
    if(row[1]==1509949420 or row[1]==1375731700 or row[1]== 1417674740 or row[1]==1501560820 or row[1]== 1493172220):
        print(tup)
    # resultsNoID.append(tup)

for row in results2:
    tup = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    resultsNoID2.append(tup)
    # resultsNoID.append(tup)

resultsNoID1.sort()
resultsNoID2.sort()
tsList = []
for i in range(1369310940, 1543207080, 40):
    tsList.append(i)

# print("first1", resultsNoID1.pop(0))
# print("last1", resultsNoID1.pop())
# print("first2", resultsNoID2.pop(0))
# print("last2", resultsNoID2.pop())
#
tsListResults.sort()
diff = list(set(tsList).symmetric_difference(set(tsListResults)))
# diff.sort()
# for row in diff:
#     print(row)
# results12NoID = sorted(list(set().union(results1NoID, results2NoID)))

# resultsNoIDClean = list(set(resultsNoID))
# resultsNoIDClean.sort()
# for row in resultsNoIDClean:
#     print(row)
# # id += 1
# # print(id)
# # if (row in results1NoID):
# # else:
# # lastID += 1
# cur3.executemany(
#     "INSERT INTO candles_BTC_LTC (start,open,high,low,close,vwp,volume,trades) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
#     (resultsNoIDClean))
# conn3.commit()
