from re import search
from os import popen
from src.api.connect import session
from src.api.ol.models import AccountBalance
from sqlalchemy.sql.expression import func
from typing import AnyStr


def get_wallet_type(address: AnyStr) -> AnyStr:
    """
    Get the wallet type for a given address.
    IMPORTANT: Whether the address exists on the chain or not, is not checked here.
               When an address is passed that doesn't exist, 'N' will be returned.
    :param address: the wallet address for which the wallet type needs to be returned
    :return: E = Error, S = Slow, C = Community, N = Normal
    """
    # check if the address is valid
    regex_out = search("[a-fA-F0-9]{32}$", address)
    if not regex_out:
        return 'E'

    # check if value is already known
    res = session\
        .query(AccountBalance.wallet_type, AccountBalance.account_type)\
        .filter(func.lower(AccountBalance.address)==address.lower())\
        .first()
    if res:
        if res[1] == 'community':
            return 'C'
        elif res[0] == 'S':
            return res[0]
    
    # check the chain if value is unknown or 'O', as it could have changed since last update
    with popen(f"ol -a {address} query -r | sed -n '/SlowWallet/,/StructTag/p'") as f:
        for elem in f.readlines():
            if 'SlowWallet' in elem:
                return 'S'

    return 'N'
