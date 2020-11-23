import logging
import os
import datetime
import time

from binance.client import Client
from typing import Optional, Dict, Any, List
from colorprint import ColorPrint
from colorama import Fore, Back, Style, init


path = "./keys.env"
load_dotenv(dotenv_path=path, verbose=True)

logging.basicConfig(level=logging.INFO, format=(
    Fore.BLUE + "[+] " + Style.RESET_ALL + "%(message)s "))


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
            # result["origType"]
            # result["avgPrice"]
            # result["origQty"]
            # result["symbol"]
            # result["reduceOnly"]
            # result["side"]

            self.log.green((f'{result["origType"]} order'
                            f'--- market:{result["symbol"]}'
                            f'size: {result["origQty"]}'
                            f'price: { result["avgPrice"]}'
                            f'side: {result["side"]}'
                            f'reduceOnly: {result["reduceOnly"]}'))

        except Exception as e:
            self.log.red(f'Failed to create order for order: {kwargs}')

    ############################
        # -PLACE CONDITIONAL ORDER
    ############################
    def create_conditional_order(self, **kwargs) -> None:
        try:
            result = self.client.futures_create_order(**kwargs)
            self.log.green((f'{result["origType"]} order'
                            f'--- market:{result["symbol"]}'
                            f'size: {result["origQty"]}'
                            f'price: {result["stopPrice"]}'
                            f'side: {result["side"]}'
                            f'reduceOnly: {result["reduceOnly"])'))

        except Exception as e:
            self.log.red(f'Failed to create order for order: {kwargs} -- {e}')
        ############################
        # -CANCEL ORDERS
        ############################

    def cancel_all_orders(self) -> None:
        try:
            result = self.client.futures_cancel_all_open_orders(
                symbol=self.market)
            self.log.green(f'CANCEL ALL ORDER: {result["msg"]}')
        except Exception as e:
            self.log.red(
                f'Unable to delete all orders in cancel_all_orders() -- {e}')

    def cancel_order(self, orderId) -> None:
        data = {"symbol": self.market,
                "orderId": orderId}
        try:
            result = self.client.futures_cancel_order(self, **data)
            self.log.green((f'CANCEL ORDER ---'
                            f'type: {result["type"]}'
                            f'symbol: {result["symbol"]}'
                            f'qty: {result["origQty"]}'
                            ))
        except Exception as e:
            self.log.red(f'Failed to cancel_order {orderId}-- {e}')

        ############################
        # -GET OPEN ORDERS
        ############################

    def get_open_orders(self) -> None:
        try:
            results = self.client.futures_get_open_orders(symbol=self.market)
            for result in results:
                self.log.green((f'{result["origType"]} order'
                                f'--- market:{result["symbol"]}'
                                f'size: {result["origQty"]}'
                                f'price: {result["stopPrice"]}'
                                f'side: {result["side"]}'
                                f'reduceOnly: {result["reduceOnly"]}'))
        except Exception as e:
            pass

        ############################
        # -GET POSITION
        ############################

    def get_positions(self, show_avg_price: bool = False) -> List[dict]:
        try:
            return self.client.futures_position_information()

        except expression as identifier:
            self.log.red(f'Unable to get positions information')

    def get_position(self, name: str) -> dict:
        try:
            if name:
                try:
                    result = next(filter(lambda x: x["symbol"] name.upper(), self.get_positions()), None)
                    self.log.green((f'Current POSITION:'
                                    f'symbol: {result["symbol"]}'
                                    f'entryPrice: {result["entryPrice"]}'
                                    f'liquidation: {result["liquidationPrice"]}'
                                    f'side: {result["positionSide"]}'
                                    f'size: {result["positionAmt"]}'
                                    f'unPNL: {result["unRealizedProfit"]}'))
            else:
                results = self.get_positions()
                for result in results:
                    self.log.green((f'Current POSITION:'
                                    f'symbol: {result["symbol"]}'
                                    f'entryPrice: {result["entryPrice"]}'
                                    f'liquidation: {result["liquidationPrice"]}'
                                    f'side: {result["positionSide"]}'
                                    f'size: {result["positionAmt"]}'
                                    f'unPNL: {result["unRealizedProfit"]}'))
        except Exception as e:
            self.log.red(
                f'Unable to fetch get_position, please check your input -- {e}')

        ##############################
        # -ORDER CLEANUP
        ###############################


def _get_time_offset(self):
    res = self.b.get_server_time()
    return res['serverTime'] - int(time.time() * 1000)


def synced(self, fn_name, **args):
    args['timestamp'] = int(time.time() - self.time_offset)
    return getattr(self.b, fn_name)(**args)
