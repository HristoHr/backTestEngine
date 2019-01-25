import glob
import sqlite3
import csv
import time
import pandas as pd

fdateList = []

scraper_files = glob.glob('BitmexTradeData/*.csv')  # returns an array of filenames
for i in range(len(scraper_files)):
    filter = scraper_files[i].split("/")[1][3]
    if (int(filter) < 600):
        fdateList.append(scraper_files[i])
    # dateStr = scraper_files[i]  # .split("/")[1].strip(".csv")
    # fdateList.append(dateStr)

fdateList.sort()

# 2015-01-01D04:58:37.857732000
# ts = int(time.mktime(time.strptime('2015-01-01D04:58:37.857732000', '%Y-%m-%dD%H:%M:%S.%f')))# - time.timezone
# print(ts)

symbol = "LTCXBT"
chunkSize = 100000
csvList = []
con = sqlite3.connect("bitmex.db")
c = con.cursor()
c.execute("CREATE TABLE IF NOT EXISTS " + symbol + " (timestamp integer,size real,price real)")

for i in range(0, len(fdateList)):
    # print(fdateList[i])
    # with open(fdateList[i]) as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader = pd.read_csv(fdateList[i], chunksize=chunkSize, sep=',')
    df = pd.DataFrame(csv_reader.get_chunk(chunkSize))
    for j in range(0, chunkSize):
        try:
            if df.loc[j]['symbol'] == symbol:
                ts = int(time.mktime(time.strptime(str(df.loc[j]['timestamp'])[:-3], '%Y-%m-%dD%H:%M:%S.%f')))
                tup = (ts, float(df.loc[j]['size']), float(df.loc[j]['price']))
                csvList.append(tup)
                print(tup)
        except KeyError:
            break
        # con.executemany("insert into person(firstname, lastname) values (?, ?)", persons)
if len(csvList) > 0:
    print(csvList)
    c.executemany("INSERT INTO %s VALUES (?,?,?)" % symbol, csvList)
    con.commit()
con.close()
# 2015-12-13D04:15:11.901546000
