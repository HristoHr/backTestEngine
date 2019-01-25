import glob
import sqlite3
import csv
import time;

conn = sqlite3.connect('gdax_0.1.db')
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_BTC_LTC")  # WHERE start >?", (1420160461, ))
results1 = cur.fetchall()

conn2 = sqlite3.connect('gdaxLTC.db')
cur2 = conn2.cursor()
cur2.execute("SELECT * FROM quotes_BTC_LTC")  # WHERE start >?", (1420160461, ))
results2 = cur2.fetchall()

for i in range(0, len(results1)):
    if(results1[i] != results2[i]):
        print("Different")

# tsListResults = []
#
# # print(results1.pop(0))
# # print(results1.pop())
#
# for row in results1:
#     tup = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
#     #print(tup)
#     tsListResults.append(row[1])
#     # if (row[1] == 1509949420 or row[1] == 1375731700 or row[1] == 1417674740 or row[1] == 1501560820 or row[1] == 1493172220):
#     #     print(tup)
#
# #tsListResults.sort()
#
# tsList = []
# for i in range(1471407360, 1504213860, 60):
#     tsList.append(i)
#
# # diff = list(set(tsList) - (set(tsListResults)))
# diff = list(set(tsList).symmetric_difference(set(tsListResults)))
# diff.sort()
# for row in diff:
#     print(row)
#
# print("Start", min(tsListResults))
# print("End", max(tsListResults))
