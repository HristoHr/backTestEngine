action = "openSell"
sellQuantity = equity
if ((openBuyPrice - price) == lossTarget + openAboveCurrentPrice):
# openSellPrice = price + openAboveCurrentPrice
#     sellType = "loss"
openSellPrice = openBuyPrice + profitTarget
sellQuantity = equity
sellType = "profit"
# if ((openBuyPrice - price) == lossTarget + openAboveCurrentPrice):
#     openSellPrice = price + openAboveCurrentPrice
#     sellType = "loss"
print("Open sell at: ", openSellPrice, "Sell Quantity", sellQuantity)
elif (action == "openSell"):
if (price >= openSellPrice):
    if (quantity >= sellQuantity):
        action = "sell"
        if (sellType == "profit"):
            profit += profitTarget
        else:
            profit -= profitTarget
        buyQuantity = equity
        sellQuantity = 0
        print("Close sell ", sellType, " at: ", price, "Sell Quantity", sellQuantity)
        print("Profit", profit)
    else:
        sellQuantity -= quantity
        print("Partially fill sell ", sellType, " at: ", price, "Sell Quantity", sellQuantity)

#
# Buy fill
# Sell Take Profit fill
# Sell Stop Loss fill

# SLIPAGE ATTEMPT
 elif (action == "openSellLoss"):
                if (quantity >= sellQuantity):
                    action = "sellLoss"
                    sum_ = 0
                    len_ = len(takerListPrice)
                    avrSellPrice = 0
                    for i in range(len_):
                        sum_ += takerListPrice[i]*takerListQuantity[i]

                    avrSellPrice = sum_/len_
                    print("Close taker sell at avr price: ", avrSellPrice)
                    avrSlippage = openSellPrice-avrSellPrice
                    print("Close taker sell at: slippage", avrSlippage)
                    loss = (profitTarget + avrSlippage + fee*avrSellPrice)
                    print("Loss", avrSlippage)
                    profit -= loss
                    buyQuantity = equity
                    sellQuantity = 0
                else:
                    sellQuantity -= quantity
                    takerListPrice.append(price)
                    takerListQuantity.append(quantity)
                    print("Partially fill taker sell at: ", price, "Quantity", quantity)
