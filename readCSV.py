import pandas as pd
import csv

chunkSize = 100000

reader = pd.read_csv("BitmexTradeData/20160101.csv", chunksize=chunkSize)
#names=["timestamp",	"symbol",	"side",	"size",	"price", "tickDirection", "trdMatchID",	"grossValue","homeNotional"	"foreignNotional"])
#

# print(reader.get_chunk(1))
# print(chunk['ts'])
# list = chunk['ts']
# df = pd.DataFrame(reader.get_chunk(10))
# for i in range(0, chunkSize):
#     print(df.loc[i]['quantity'])
# readCSV = list(csv.reader(chunk, delimiter=','))
# for row in readCSV:
#     print(row[0])
# # for index in range(0, len(readCSV), 1):
# #     print(readCSV[index])
#
# # readCSV = list(chunk)
# # print(readCSV[1])
# chunkSize = 100000
df = pd.DataFrame(reader.get_chunk(chunkSize))
for i in range(0, chunkSize):
    try:
        print(df.loc[i]['timestamp'])
    except KeyError:
        break

# for chunk in pd.read_csv("BitmexQuotes/20170101.csv", chunksize=chunkSize, names=["timestamp",	"symbol",	"side",	"size",	"price",	"tickDirection", "trdMatchID",	"grossValue",	"homeNotional"	"foreignNotional"]):
#
#     chunkCount += 1
#     print(df.loc[chunkCount]['timestamp'])
#      #list = chunk['ts']
