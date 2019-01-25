import csv
import time

# with open('coinbaseUSD100000.csv', encoding="utf16") as csvfile:
#     # with open('coinbaseUSD100000.csv') as csvfile:
#     tsList = []
#     quantityList = []
#     readCSV = list(csv.reader(csvfile, delimiter=','))
#     for row in readCSV:
#         tsList.append(int(row[0]))
#         quantityList.append(float(row[2]))
ts = int(time.time())
changeDirectionCount = 1
direction = 0
j = 0
price = 6000

with open('testBuySell.csv', mode='w') as test_csv:
    csv_writer = csv.writer(test_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([ts, price, 0.1])
    for i in range(0, 10000):
        j += 1
        if (price % 10 == 0):
            changeDirectionCount += 1
            j = 0
        if (changeDirectionCount % 2 == 0):
            price += 1
        else:
            price -= 1
        print(ts + i, price, 0.1)
        csv_writer.writerow([ts + i,price, 0.1])
