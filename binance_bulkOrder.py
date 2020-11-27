import logging
import os
import datetime
import time
import collections

from binance.client import Client
from typing import Optional, Dict, Any, List
from colorprint import ColorPrint
from colorama import Fore, Back, Style, init
from dotenv import load_dotenv


path = "./keys.env"
load_dotenv(dotenv_path=path, verbose=True)

logging.basicConfig(
    level=logging.INFO, format=(Fore.BLUE + "[+] " + Style.RESET_ALL + "%(message)s ")
)


class BinanceClient:
    def __init__(self) -> None:
        self._api_key = os.getenv("BINANCE_TEST_API")
        self._api_secret = os.getenv("BINANCE_TEST_SECRET")
        self.client = Client(self._api_key, self._api_secret)
        self.log = ColorPrint()
        self.market = None
        self.orderSide = None
        self.fatFinger = None

    ############################
    # -PLACE ORDER
    ############################
    def create_order(self, **kwargs) -> None:

        try:
            result = self.client.futures_create_order(**kwargs)
            self.log.green(
                (
                    f'{result["origType"]}:'
                    f'{result["symbol"]}, '
                    f'size:{result["origQty"]}, '
                    f'price:{ result["price"]}, '
                    f'side:{result["side"]}, '
                    f'reduceOnly:{result["reduceOnly"]} '
                )
            )

        except Exception as e:
            self.log.red(f"Failed to create order for order: {kwargs} \n message: {e}")

    ############################
    # -PLACE CONDITIONAL ORDER
    ############################
    def create_conditional_order(self, **kwargs) -> None:
        try:
            result = self.client.futures_create_order(**kwargs)

            self.log.green(
                (
                    f'{result["origType"]}:'
                    f'{result["symbol"]}, '
                    f'size:{result["origQty"]}, '
                    f'price:{ result["stopPrice"]}, '
                    f'side:{result["side"]},'
                    f'reduceOnly:{result["reduceOnly"]}'
                )
            )

        except Exception as e:
            self.log.red(f"Failed to create order for order: {kwargs} \n message:{e}")

    ############################
    # -CANCEL ORDERS
    ############################

    def cancel_all_orders(self) -> None:
        try:
            result = self.client.futures_cancel_all_open_orders(symbol=self.market)
            self.log.green(f'CANCEL ALL ORDER: {result["msg"]}')
        except Exception as e:
            self.log.red(
                f"Unable to delete all orders in cancel_all_orders() \n message: {e}"
            )

    def cancel_order(self, orderId) -> None:
        data = {
            "symbol": self.market,
            "orderId": float(orderId),
        }  # make sure this is float
        try:
            result = self.client.futures_cancel_order(**data)
            self.log.green(
                (
                    f"CANCEL ORDER ---"
                    f'type: {result["type"]} '
                    f'symbol: {result["symbol"]} '
                    f'qty: {result["origQty"]}'
                )
            )
        except Exception as e:
            self.log.red(f"Failed to cancel_order {orderId} \n message: {e}")

        ############################
        # -GET OPEN ORDERS
        ############################

    def get_open_orders(self) -> None:
        try:
            results = self.client.futures_get_open_orders(symbol=self.market)
            for result in results:
                self.log.green(
                    (
                        f'{result["origType"]}:'
                        f'{result["symbol"]} '
                        f'size:{result["origQty"]} '
                        f'price:{result["stopPrice"]} '
                        f'side:{result["side"]} '
                        f'reduceOnly:{result["reduceOnly"]} '
                        f'orderID:{result["orderId"]}'
                    )
                )
        except Exception as e:
            self.log.red(
                f"Unable to get_open_orders for current market : {self.market}"
            )

        ############################
        # -GET POSITION
        ############################

    def get_position(self, symbol: str = None) -> dict:
        try:
            if symbol:
                results = self.client.futures_position_information(
                    symbol=symbol.upper()
                )
                result = results[0]
                entryPrice = round(float(result["entryPrice"]), 2)
                liquidation = round(float(result["liquidationPrice"]), 2)
                unPNL = round(float(result["unRealizedProfit"]), 2)
                self.log.green(
                    (
                        f"POSITION:"
                        f'{result["symbol"]} '
                        f"entryPrice:{entryPrice} "
                        f"liquidation:{liquidation} "
                        f'side:{result["positionSide"]} '
                        f'size:{result["positionAmt"]} '
                        f"unPNL:{unPNL} "
                    )
                )
            else:
                results = self.client.futures_position_information()
                for result in results:
                    if float(result["positionAmt"]) > 0:
                        entryPrice = round(float(result["entryPrice"]), 2)
                        liquidation = round(float(result["liquidationPrice"]), 2)
                        unPNL = round(float(result["unRealizedProfit"]), 2)
                        self.log.green(
                            (
                                f"POSITION:"
                                f'{result["symbol"]} '
                                f"entryPrice:{entryPrice} "
                                f"liquidation:{liquidation} "
                                f'side:{result["positionSide"]} '
                                f'size:{result["positionAmt"]} '
                                f"unPNL:{unPNL}"
                            )
                        )
        except Exception as e:
            self.log.red(
                f"Unable to fetch get_position, please check your input -- {e}"
            )

        ##############################
        # -ORDER CLEANUP
        ###############################

    def place_order_cleanup(self, currCommand):
        try:
            side = currCommand[0].upper() if len(currCommand) > 0 else None
            self.orderSide = side
            size = float(currCommand[1]) if len(currCommand) > 1 else 0
            if len(currCommand) > 2:
                if "@" in currCommand[2]:
                    price = currCommand[2].replace("@", "")
                else:
                    price = currCommand[2]
            else:
                price = None
            type = "LIMIT" if len(currCommand) > 2 else "MARKET"

            if type == "LIMIT":
                data = {
                    "symbol": self.market,
                    "side": side,
                    "type": type,
                    "quantity": float(size) if size else None,
                    "price": float(price) if price else None,
                    "timeInForce": "GTC",
                }
            else:
                data = {
                    "symbol": self.market,
                    "side": side,
                    "type": type,
                    "quantity": float(size) if size else None,
                }

            self.log.green(data)
            if size:
                if float(size) < float(self.fatFinger):
                    self.create_order(**data)

        except Exception as e:
            self.log.red(f"Error in place_order_cleanup() , please check entry: {e}")

    def place_conditional_order_cleanup(self, currCommand):

        try:
            if len(currCommand) > 4:
                if "@" in currCommand[4]:
                    limitPrice = currCommand[4].replace("@", "")
                else:
                    limitPrice = currCommand[4]
            else:
                limitPrice = None

            type = currCommand[0] if len(currCommand) > 0 else None
            if type == "tp":
                if limitPrice:
                    type = "TAKE_PROFIT"
                else:
                    type = "TAKE_PROFIT_MARKET"
            if type == "trail":
                type = "TRAILING_STOP_MARKET"
            if type == "stop":
                if limitPrice:
                    type = "STOP"
                else:
                    type = "STOP_MARKET"

            size = currCommand[1] if len(currCommand) > 1 else None
            if len(currCommand) > 2:
                if "@" in currCommand[2]:
                    price = currCommand[2].replace("@", "")
                else:
                    price = currCommand[2]
            else:
                price = None

            try:

                if self.orderSide and not limitPrice:
                    side = "BUY" if self.orderSide == "SELL" else "SELL"
                elif len(currCommand) > 3:
                    side = currCommand[3].upper()
                else:
                    self.log.red(
                        f"Error in placing conditional order,need to assign a side order"
                    )
            except Exception as e:
                self.log.red("cleanup conditional orderSide not assign correctly")
            data = {}
            if limitPrice:
                data = {
                    "symbol": self.market,
                    "side": side,
                    "type": type,
                    "quantity": float(size) if size else None,
                    "stopPrice": float(price) if price else None,
                    "price": float(limitPrice) if limitPrice else None,
                    "reduceOnly": True,
                }

            else:
                data = {
                    "symbol": self.market,
                    "side": side,
                    "type": type,
                    "quantity": float(size) if size else None,
                    "stopPrice": float(price) if price else None,
                    "reduceOnly": True,
                }
            self.log.green(data)
            if size and float(size) < float(self.fatFinger):
                if price:
                    self.create_conditional_order(**data)
                else:
                    self.log.red(
                        f"Error in placing conditional order cleanup, missing stopPrice or limit_price"
                    )
            else:
                self.cp.red(
                    f"Error in placing conditional order cleanup,need size order or exceeds fatFinger: {self.fatFinger}"
                )
        except Exception as e:
            self.log.red(f"Error in place_conditional_order_cleanup: {e}")


def _get_time_offset(self):
    res = self.b.get_server_time()
    return res["serverTime"] - int(time.time() * 1000)


def synced(self, fn_name, **args):
    args["timestamp"] = int(time.time() - self.time_offset)
    return getattr(self.b, fn_name)(**args)
