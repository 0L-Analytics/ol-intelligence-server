from re import search
from os import popen


def get_wallet_type(address):
    """
    Checks if a given address is a slow wallet.
    :param address: the wallet address to check
    :return: True if the wallet is a slow wallet
    """
    # check if the address is valid
    regex_out = search("[a-fA-F0-9]{32}$", address)
    if not regex_out:
        return False

    print("test")

    # We are checking both 'SlowWallet' and 'Community' occurence in the query output
    with popen(f"ol -a {address} query -r | sed -n '/SlowWallet/,/StructTag/p'") as f:
        print(f.readline())
        for elem in f.readlines():
            print(elem)
            if 'SlowWallet' in elem:
                return True
    return False
