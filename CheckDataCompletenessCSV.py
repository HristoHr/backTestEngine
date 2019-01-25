import glob
import numpy
from datetime import date, timedelta

# 20141122
# 20181206
d1 = date(2014, 11, 22)  # start date
d2 = date(2018, 12, 6)  # end date

delta = d2 - d1  # timedelta

dateList = []
fdateList = []
for i in range(delta.days + 1):
    dateStr = str(d1 + timedelta(i)).replace("-", "")
    dateList.append(dateStr)
    # print(dateStr)

scraper_files = glob.glob('BitmexTradeData/*.csv')  # returns an array of filenames
for i in range(len(scraper_files)):
    dateStr = scraper_files[i].split("/")[1].strip(".csv")
    fdateList.append(dateStr)
    # print(dateStr)
    # fdateList.append()

fdateList.sort()

print(len(fdateList))
print((len(dateList)))
print(list(set(dateList).symmetric_difference(set(fdateList))))
print(list(set(fdateList).symmetric_difference(set(dateList))))
print(list(set(dateList) - (set(fdateList))))
print(list(set(fdateList) - (set(dateList))))
print(numpy.array(dateList) == numpy.array(fdateList))
print(numpy.array(fdateList) == numpy.array(dateList))
print(fdateList == dateList)
