import os

from time import sleep

from config import Config
from model import PaymentEvent, ChainEvent, Epoch, NetworkStat


if __name__ == "__main__":

    if Config.ENV == "development":
        ...

    i = 1
    while i < 10:
        sleep(1)
        print(f"i={i}")
        i += 1
