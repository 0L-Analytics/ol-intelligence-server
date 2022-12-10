from requests import get 
from datetime import datetime
from typing import List
from config import Config


def get_wallet_type_flag(address_list: List) -> List:
    """
    Gets wallet_types for addresses in the given list
    :param address_list: 
    :return: list of dictionaries with address and wallet_type
    """
    list_out = []
    try:
        for address in address_list:
            api_url = f"{Config.TOOLS_URI}/ol/wallettype?address={address}"
            result = get(api_url, timeout=15).json()
            list_out.append(result)
    except Exception as e:
        print(f"[{datetime.now()}]:{e}")
        list_out = []
    return list_out
