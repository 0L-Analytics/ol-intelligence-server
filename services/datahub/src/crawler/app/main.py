from json import load
from time import sleep
from datetime import datetime

from config import Config
from crawler.app.oldata import (
    load_account_balances_for_acc_type, 
    load_account_txs_for_addr_list, 
    load_events_for_addr_list
)
from crawler.app.tools import update_wallet_type_flag


def load_data() -> None:
    """
    Builds the community wallet list and loads events.
    :return: no return value
    """
    acc_type_list = ["community", "validator", "miner", "basic"]

    try:
        # Load community wallets
        f = open(f'{Config.ASSETS_DIR}/wallets.json')
        data = load(f)
        address_list = [wallet['account'] for wallet in data['community']]
        f.close()

        # FOR TESTING ONLY
        if Config.ENV == "development":
            # address_list = ["3A6C51A0B786D644590E8A21591FA8E2", "C906F67F626683B77145D1F20C1A753B"]
            ...

        # Load data
        load_events_for_addr_list(address_list=address_list)
        load_account_txs_for_addr_list(address_list=address_list)
        
        for acc_type in acc_type_list:
            load_account_balances_for_acc_type(acc_type)
        
        update_wallet_type_flag()

    except Exception as e:
        print(f"[{datetime.now()}]:{e}")


if __name__ == "__main__":

    # Initial sleep time to get db seeded
    initial_sleep = int(Config.INITIAL_SLEEP_SECS)
    print(f"[{datetime.now()}] Waiting {initial_sleep} secs")
    sleep(initial_sleep)

    # Determine sleepy time for every cyclus
    sleepy_time = int(Config.SLEEP_MINS)

    if Config.ENV == "development":
        ...

    while True:
        # Load community wallets data
        print(f"[{datetime.now()}] Start loading data.")
        load_data()

        # Sleepy time before start next cyclus
        print(f"[{datetime.now()}] End crawling. Sleep {sleepy_time} minutes.")
        sleep(sleepy_time * 60)
