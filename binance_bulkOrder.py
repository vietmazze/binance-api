from binance.client import Client


client = Client(test_api, test_secret)

client.futures_account_balance()


"""
-CREATE LIMIT ORDER 
LIMIT	timeInForce, quantity, price

data = {"symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": "0.01",
        "price": "15000",
        "timeInForce": "GTC"
        }

*order= client.futures_create_order(**data)


-CREATE MARKET ORDER
data = {"symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": "0.01",
        }

*order = client.futures_create_order(**data)
-CREATE STOP MARKET ORDER
-CREATE TP MARKET ORDER

data = {"symbol": "BTCUSDT",
        "side": "SELL",
        "type": "STOP_MARKET",
        "quantity": "0.01",
        "stopPrice": 14000
        }

data = {"symbol": "BTCUSDT",
        "side": "SELL",
        "type": "TAKE_PROFIT_MARKET",
        "quantity": "0.01",
        "stopPrice": 20000
        }


-CREATE STOP LIMIT ORDER
-CREATE LIMIT TP ORDER




-CREATE BULK ORDER



-RETURN VALUE FOR NEW ORDER

{
{'orderId': 195019720,
 'symbol': 'AAVEUSDT',
 'status': 'NEW',
 'clientOrderId': 'gnQbxSgidHejLQPwHH8tmc',
 'price': '0',
 'avgPrice': '0.0000',
 'origQty': '0.1',
 'executedQty': '0',
 'cumQty': '0',
 'cumQuote': '0',
 'timeInForce': 'GTC',
 'type': 'MARKET',
 'reduceOnly': False,
 'closePosition': False,
 'side': 'BUY',
 'positionSide': 'BOTH',
 'stopPrice': '0',
 'workingType': 'CONTRACT_PRICE',
 'priceProtect': False,
 'origType': 'MARKET',
 'updateTime': 1605804380025}



-GET CURRENT FUTURES POSITION

[{'symbol': 'AAVEUSDT',
  'positionAmt': '0.0',
  'entryPrice': '0.0000',
  'markPrice': '80.17839843',
  'unRealizedProfit': '0.00000000',
  'liquidationPrice': '0',
  'leverage': '20',
  'maxNotionalValue': '25000',
  'marginType': 'cross',
  'isolatedMargin': '0.00000000',
  'isAutoAddMargin': 'false',
  'positionSide': 'BOTH'}]


*client.futures_position_information(symbol="AAVEUSDT")




-GET OPEN ORDERS FOR SPECIFIC SYMBOL
[{'orderId': 9293682339,
  'symbol': 'BTCUSDT',
  'status': 'NEW',
  'clientOrderId': 'dCgK17W8BHDJGJ37mq7LRY',
  'price': '0',
  'avgPrice': '0.00000',
  'origQty': '0.010',
  'executedQty': '0',
  'cumQuote': '0',
  'timeInForce': 'GTC',
  'type': 'STOP_MARKET',
  'reduceOnly': False,
  'closePosition': False,
  'side': 'SELL',
  'positionSide': 'BOTH',
  'stopPrice': '14000',
  'workingType': 'CONTRACT_PRICE',
  'priceProtect': False,
  'origType': 'STOP_MARKET',
  'time': 1605805059776,
  'updateTime': 1605805311129}]

*client.futures_get_open_orders(symbol="BTCUSDT")




-GET SPECIFIC ORDER BY ORDERID
[{'orderId': 9293682339,
  'symbol': 'BTCUSDT',
  'status': 'NEW',
  'clientOrderId': 'dCgK17W8BHDJGJ37mq7LRY',
  'price': '0',
  'avgPrice': '0.00000',
  'origQty': '0.010',
  'executedQty': '0',
  'cumQuote': '0',
  'timeInForce': 'GTC',
  'type': 'STOP_MARKET',
  'reduceOnly': False,
  'closePosition': False,
  'side': 'SELL',
  'positionSide': 'BOTH',
  'stopPrice': '14000',
  'workingType': 'CONTRACT_PRICE',
  'priceProtect': False,
  'origType': 'STOP_MARKET',
  'time': 1605805059776,
  'updateTime': 1605805311129}]
  

*client.futures_get_order(symbol="BTCUSDT",orderId="9293682339")



-CANCEL ALL OPEN ORDERS
{'code': 200, 'msg': 'The operation of cancel all open order is done.'}

data = {"symbol":"BTCUSDT"}

*client.futures_cancel_all_open_orders(**data)
"""
