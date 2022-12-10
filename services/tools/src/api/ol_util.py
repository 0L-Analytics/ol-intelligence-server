import os
import re
from typing import AnyStr


def is_slow_wallet(address: AnyStr) -> bool:
    """
    Checks if a given address is a slow wallet.
    :param address: the address to check
    :return: Boolean True if the wallet is a slow wallet, else False
    """
    # check if the address is valid
    regex_out = re.search("[a-fA-F0-9]{32}$", address)
    if not regex_out:
        return False

    # We are checking both 'SlowWallet' and 'Community' occurence in the query output
    with os.popen(f"ol -a {address} query -r | grep 'SlowWallet\|Community'") as f:
        for elem in f.readlines():
            if 'SlowWallet' in elem:
                return True
            elif 'Community' in elem:
                # Here we assume that community wallets are by default slow...
                return True
    
    return False


if __name__ == "__main__":
    
    test_list = [
        "5F8AC83A9B3BF2EFF20A6C16CD05C111", # SLOW basic wallet
        "2BFD96D8A674A360B733D16C65728D72", # normal basic wallet
        "1367B68C86CB27FA7215D9F75A26EB8F", # SLOW community wallet
        "5335039ab7908dc38d328685dc3b9141", # normal miner wallet
        "7e56b29cb23a49368be593e5cfc9712e", # SLOW validator wallet
        "82a1097c4a173e7941e2c34b4cbf15b4", # normal miner wallet
        "5e358589da97d5f08bf3a7462a112ae6", # normal miner wallet
        "19E966BFA4B32CE9B7E23721B37B96D2", # SLOW another community wallet
        "cd0fa23141e9e5e348b33c5da51f211d", # normal miner wallet
        "f100a2878d61bab8554aed256feb8001", # normal miner wallet
        "4be425e5306776a0bd9e2db152b856e6", # SLOW miner wallet
        "7103da7bb5bb15eb7e72b6db16147f56", # normal miner wallet
        "74745f89883134d270d0a57c6c854b4b", # normal miner wallet
    ]

    for addr in test_list:
        if is_slow_wallet(addr):
            print(f"{addr} is a slow (or community) wallet!")
    