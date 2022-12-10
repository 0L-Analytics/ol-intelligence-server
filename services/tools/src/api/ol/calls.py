from re import search
from os import popen
from src.api.connect import session
from src.api.ol.models import AccountBalance
from sqlalchemy.sql.expression import func
# from sqlalchemy import Integer
from typing import AnyStr, Any


def get_wallet_type(address: AnyStr) -> Any:
    """
    Checks if a given address is a slow wallet.
    :param address: the wallet address to check
    :return: True if the wallet is a slow wallet
    """
    # check if the address is valid
    regex_out = search("[a-fA-F0-9]{32}$", address)
    if not regex_out:
        return False

    # check if value is already known
    res = session\
        .query(AccountBalance.wallet_type)\
        .filter(func.lower(AccountBalance.address)==address.lower())\
        .first()
    if res:
        if res[0] == 'S':
            return True
        if res[0] == 'C':
            return False
    
    # check the chain if value is unknown or 'O', as it could have changed since last update
    with popen(f"ol -a {address} query -r | sed -n '/SlowWallet/,/StructTag/p'") as f:
        print(f.readlines())
        for elem in f.readlines():
            print("peup")
            if 'SlowWallet' in elem:
                return True

    return False
