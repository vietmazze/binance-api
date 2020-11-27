import time
import logging
import numpy as np
import collections
from dotenv import load_dotenv

from binance_bulkOrder import BinanceClient
from typing import Optional, Dict, Any, List
from colorprint import ColorPrint
from colorama import Fore, Back, Style, init

path = "./keys.env"
load_dotenv(dotenv_path=path, verbose=True)

logging.basicConfig(
    level=logging.INFO, format=(Fore.BLUE + "[+] " + Style.RESET_ALL + "%(message)s ")
)


def process_command(binance, userInput):

    commands = collections.deque()
    try:
        for input in userInput.split(";"):
            # [buy 1 @8500, sell 1 @8600]
            commands.append(input.strip())
    except Exception as e:
        cp.red(f" failted ot loop commands {e}")
    while commands:
        currCommand = commands.popleft().split(" ")
        try:
            ######################
            # -PLACING ORDER
            ######################
            if currCommand[0] == "buy" or currCommand[0] == "sell":
                binance.place_order_cleanup(currCommand)

            ######################
            # -PLACING CONDITIONAL ORDER
            ######################

            elif (
                currCommand[0] == "stop"
                or currCommand[0] == "tp"
                or currCommand[0] == "trail"
            ):

                binance.place_conditional_order_cleanup(currCommand)

            ######################
            # -SHOW OPEN ORDERS
            ######################
            elif currCommand[0] == "order":
                binance.get_open_orders()

            ######################
            # -CANCEL ORDERS
            ######################
            elif currCommand[0] == "cancel":
                conditional_id = currCommand[1] if len(currCommand) >= 2 else None
                # diff types of cancel

                if binance.market is not None:
                    if conditional_id and conditional_id.isnumeric():
                        binance.cancel_order(orderId=conditional_id)
                    else:
                        binance.cancel_all_orders()
                else:
                    cp.red(f"Missing market to delete orders, please assign instrument")
            ######################
            # -LOCKING INSTRUMENT
            ######################
            elif currCommand[0] == "instrument" or currCommand[0] == "i":
                if len(currCommand) < 2:
                    cp.green(f"Current MARKET: {binance.market}")
                elif currCommand[1]:
                    binance.market = currCommand[1].upper()
                    cp.green(f"Assign new MARKET: {binance.market}")

            ######################
            # -SET FATFINGER:
            ######################
            elif currCommand[0] == "fatfinger" or currCommand[0] == "fat":
                if len(currCommand) > 1:
                    if currCommand[1]:
                        binance.fatFinger = float(currCommand[1])
                        cp.green(f"fatFinger set: {binance.fatFinger}")
                    else:
                        cp.red(
                            f"Please input only digits for fatfinger: {currCommand[1]}"
                        )
                else:
                    cp.red(f"Missing the value for fatfinger")
            ######################
            # -SHOW OPEN POSITIONS
            ######################
            elif currCommand[0] == "position":
                market = currCommand[1] if len(currCommand) > 1 else None
                if market:
                    binance.get_position(symbol=market)
                else:
                    binance.get_position()

            ######################
            # - SPLITTING ORDERS
            # ! split [sell] [0.1] into [10] from [11288] to [11355]
            ######################
            elif currCommand[0] == "split":
                try:
                    side = currCommand[1] if len(currCommand) > 1 else None
                    size = currCommand[2] if len(currCommand) > 2 else None
                    total = float(currCommand[4]) if len(currCommand) > 4 else None
                    start = float(currCommand[6]) if len(currCommand) > 6 else None
                    end = float(currCommand[8]) if len(currCommand) > 7 else None
                    limitOrder = currCommand[9] if len(currCommand) > 9 else None
                    if len(currCommand) > 8:
                        order_list = split_equal_parts(start, end, total)
                        size = float(size) / total
                        cp.green(order_list)
                        if not None in (side, size, total, start, end):

                            if side == "buy" or side == "sell":
                                while total > 0 and len(order_list) > 0:

                                    binance.place_order_cleanup(
                                        [side, float(size), str(order_list.pop())]
                                    )
                                    total -= 1
                            elif side == "stop" or side == "tp" or side == "trail":

                                while total > 0 and len(order_list) > 0:
                                    price = str(order_list.pop())

                                    binance.place_conditional_order_cleanup(
                                        [side, float(size), price, limitOrder, price]
                                    )
                                    total -= 1
                            else:
                                cp.red(
                                    f"One of the values in split order is missing, please check your command: \n {currCommand}"
                                )

                        else:
                            cp.red(
                                f"Split order requires all 9 words typed out, please check your command: \n {currCommand}"
                            )
                    else:
                        cp.red(
                            f"Split order requires all 9 words typed out, please check your command: \n {currCommand}"
                        )

                except Exception as e:
                    cp.red(f"TESTING split order {e}")

            #######################
            # - HELP COMMAND
            #######################

            elif currCommand[0] == "help" or currCommand[0] == "/help":
                show_command()

            else:
                cp.red(
                    f"Error in process_command, please use only one of those command option: buy,sell,order,cancel,position,split"
                )

        except Exception as e:
            cp.red(
                f"Error in process_command, please restart your program:  {currCommand}  \n  {e.args} "
            )


######################################
# - Calculation for splitting order
######################################


def split_equal_parts(start, end, total):
    try:
        price = [start]
        avg_price = round((end - start) / total, 4)

        while total > 2:
            curr = round(start + avg_price, 3)
            price.append(curr)
            start = curr
            total -= 1
        price.append(end)
        return price
    except Exception as e:
        cp.red(f" split_equal_parts failed -{e}")


######################################
# - Commands for bot
######################################
def show_command():
    cp.green(
        f"""
            INIT MARKET required before start:
                [instrument] [XTZ-PERP]
                [fatfinger] [#]
            BUY-SELL ORDERS:
                market order - [type] [size] - buy 1000
                limit order - [type] [size] [price] - buy 1 @1
                stop market - [type] [size] [price] - stop 1 @1
                stop limit - [type] [size] [price] [side] [limitPrice] - stop 1 @1 sell @1
                take profit market - [type] [size] [price] - tp 1 @1
                take profit limit - [type] [size] [price] [side] [limitPrice] - tp 1 @1 sell @1
            SPLIT ORDERS:
                split [type] [size] into [total] from [price 1] to [price 2] [buy/sell] 
                split order - split [sell] [0.1] into [10] from [11288] to [11355] (no buy/sell) 
                split conditional order - split [stop/tp] [0.1] into [10] from [11288] to [11355] [buy/sell]
            CANCEL ORDERS:
                cancel - cancel all orders
                cancel limit - cancel all limit buy/sell
                cancel conditional - cancel all stop/tp
                cancel 123456 - cancel specific buy/sell limit order ID
                cancel conditional 123456 - cancel specific stop/tp order ID
            SHOW ORDERS:
                order - show all limit and stops open order
                position  - show all current positions
                position [market] - show specific market"""
    )


def main(binance):
    input(
        "Welcome to Binance bot, please start by creating your market... press enter to continue"
    )
    while True:
        # main program

        try:
            while True:

                userInput = input("Command: ")
                break
            if userInput == "quit":
                break
            else:
                process_command(binance, userInput)
        except Exception as e:
            cp.red(f"Exception in calling main() {e}")


if __name__ == "__main__":
    cp = ColorPrint()
    binance = BinanceClient()
    try:
        main(binance)
    except Exception as ex:
        cp.red(ex.args)
    finally:
        exit()
