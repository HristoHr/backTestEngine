import cbpro

public_client = cbpro.PublicClient()
public_client.get_product_historic_rates('ETH-USD')
# To include other parameters, see function docstring:
histData = public_client.get_product_historic_rates('ETH-USD', granularity=60)
print(histData[0])
print(histData[1])
trades = public_client.get_product_trades(product_id='ETH-USD')
ticker = public_client.get_product_ticker(product_id='ETH-USD')
print(trades)
print(ticker)