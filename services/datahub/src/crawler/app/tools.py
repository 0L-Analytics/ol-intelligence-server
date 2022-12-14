from requests import get 
from datetime import datetime
from config import Config
from crawler.db.model import AccountBalance, session
from typing import Any


def update_wallet_type_flag(for_all: Any=False) -> None:
    """
    Updates wallet_types in the database.
    :return: None
    """
    try:
        if for_all:
            # Exclude the types that can never change
            result = session\
                .query(AccountBalance.id, AccountBalance.address, AccountBalance.wallet_type)\
                .filter(AccountBalance.wallet_type != 'S', AccountBalance.wallet_type != 'C')\
                .order_by(AccountBalance.wallet_type.desc())\
                .all()
        else:
            # Inculde only the unassigned types
            result = session\
                .query(AccountBalance.id, AccountBalance.address, AccountBalance.wallet_type)\
                .filter(AccountBalance.wallet_type == 'X')\
                .order_by(AccountBalance.wallet_type.desc())\
                .all()
        if result:
            for t in result:
                api_url = f"{Config.TOOLS_URI}/ol/wallettype?address={t[1]}"
                resp = get(api_url, timeout=15).json()
                if resp['wallet_type'] != t[2]:
                    ab = AccountBalance(
                        id = t[0],
                        wallet_type = resp['wallet_type']
                    )
                    session.merge(ab)
                    session.commit()
    except Exception as e:
        print(f"[{datetime.now()}]:{e}")
    return None
