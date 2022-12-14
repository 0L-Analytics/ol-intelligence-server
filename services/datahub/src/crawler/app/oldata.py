from requests import get
from datetime import datetime
from typing import AnyStr, List
from sqlalchemy import func

from config import Config
from crawler.db.model import (
    PaymentEvent, 
    AccountTransaction, 
    AccountBalance,
    ValidatorSet,
    session
)


def get_0l_api_data(end_point_suffix: AnyStr, output_elem: AnyStr=None, **options) -> List:
    """
    Gets data from the 0L API.
    :param end_point_suffix: the path of the endpoint at 0lexplorer.io
    :param output_elem: the child element in the output dictionary to be returned, if applicable
    :param options: options to be passed along with API call
    :return: list of elements representing a data set
    """
    try:
        option_string = ""
        if len(options) > 0 and end_point_suffix[1:]:
            for option_key in options.keys():
                if len(option_string) > 0:
                    option_string += "&"
                option_string += f"{option_key}={options[option_key]}"

        api_url = f"{Config.BASE_API_URI}{end_point_suffix}{option_string}"
        result = get(api_url, timeout=300).json()
        if output_elem and output_elem in result:
            result = result[output_elem]
    except Exception as e:
        # TODO add proper logging + throw specific exception to break when called in a loop
        print(f"[{datetime.now()}]:{e}")
        result = []
    return result


def load_events_for_addr_list(address_list: List) -> None:
    """
    Loads all the transaction for an address list into the db.
    :param address_list: list of 0L addresses
    :return: no return value
    """
    # Iterate address_list
    for address in address_list:

        # fetch payment events
        try:
            more_to_load = True
            batch_size = 1000
            while more_to_load:

                # Get last loaded sequence. This strategy assumes that 
                # all events before the highest (last loaded) sequence
                # have been loaded successfully. 
                # TODO add a consistency check for data prior to last
                # loaded sequence!
                max_seq = session\
                    .query(func.max(PaymentEvent.seq))\
                    .filter(PaymentEvent.address == address)\
                    .scalar()
                max_seq = max_seq if max_seq else 0
                
                # Get the data from the api
                result = get_0l_api_data(
                    end_point_suffix="/api/proxy/node/events?",
                    output_elem="result",
                    address=address,
                    start=max_seq,
                    limit=batch_size)
                
                # Iterate objects and store them in the db
                for pe_obj in result:
                    pe_id = session\
                        .query(PaymentEvent.id)\
                        .filter(PaymentEvent.address == address, 
                                PaymentEvent.seq == int(pe_obj['sequence_number']))\
                        .scalar()

                    o = PaymentEvent(
                        address=address,
                        amount=float(pe_obj['data']['amount']['amount']) / 1000000,
                        currency=pe_obj['data']['amount']['currency'],
                        _metadata=pe_obj['data']['metadata'],
                        sender=pe_obj['data']['sender'],
                        recipient=pe_obj['data']['receiver'],
                        type=pe_obj['data']['type'],
                        transactionkey=pe_obj['key'],
                        seq=int(pe_obj['sequence_number']),
                        height=int(pe_obj['transaction_version'])
                        )

                    if pe_id:
                        o.id = pe_id
                        session.merge(o)
                    else:
                        session.add(o)

                session.commit()

                if len(result) < batch_size:
                    more_to_load = False

        except Exception as e:
            print(f"[{datetime.now()}]:{e}")


def load_account_txs_for_addr_list(address_list: List) -> None:
    """
    Loads all the account transactions for an address list into the db.
    :param address_list: list of 0L addresses
    :return: no return value
    """
    # Iterate address_list
    for address in address_list:

        # fetch payment events
        try:
            more_to_load = True
            batch_size = 1000
            while more_to_load:

                # Get last loaded sequence. This strategy assumes that 
                # all events before the highest (last loaded) sequence
                # have been loaded successfully. 
                # TODO add a consistency check for data prior to last
                # loaded sequence!
                max_seq = session\
                    .query(func.max(AccountTransaction.sequence_number))\
                    .filter(AccountTransaction.address == address)\
                    .scalar()
                max_seq = max_seq if max_seq else 0
                
                # Get the data from the api
                result = get_0l_api_data(
                    end_point_suffix="/api/proxy/node/account-transactions?",
                    output_elem="result",
                    address=address,
                    start=max_seq,
                    limit=batch_size)
                
                # Iterate objects and store them in the db
                for pe_obj in result:
                    pe_id = session\
                        .query(AccountTransaction.id)\
                        .filter(AccountTransaction.address == address, 
                                AccountTransaction.sequence_number == int(pe_obj['transaction']['sequence_number']))\
                        .scalar()

                    o = AccountTransaction(
                        address=address,
                        sequence_number=int(pe_obj['transaction']['sequence_number']),
                        version=pe_obj['version'],
                        tx=pe_obj['transaction'],
                        hash=pe_obj['hash'],
                        vm_status=pe_obj['vm_status'],
                        gas_used=pe_obj['gas_used']
                    )

                    if pe_id:
                        o.id = pe_id
                        session.merge(o)
                    else:
                        session.add(o)

                session.commit()

                if len(result) < batch_size:
                    more_to_load = False

        except Exception as e:
            print(f"[{datetime.now()}]:{e}")


def load_account_balances_for_acc_type(account_type: AnyStr) -> None:
    """
    Loads balances for an address list into the db.
    :param address_list: list of 0L addresses
    :return: no return value
    """
    # TODO Create a account_type type
    # fetch balances
    try:           
        # Get the data from the api
        result = get_0l_api_data(
            end_point_suffix=f":444/balances?account_type={account_type}"
        )
        
        # Iterate objects and store them in the db
        for pe_obj in result:
            pe_id = session\
                .query(AccountBalance.id)\
                .filter(AccountBalance.address == pe_obj['address'])\
                .scalar()

            o = AccountBalance(
                address=pe_obj['address'],
                balance=int(pe_obj['balance']),
                account_type=pe_obj['account_type']
            )

            if pe_id:
                o.id = pe_id
                session.merge(o)
            else:
                session.add(o)

        session.commit()

    except Exception as e:
        print(f"[{datetime.now()}]:{e}")


def load_community_wallet_descriptions():
    # TODO: load wallet.json into walletdescription table
    ...


def load_active_validator_set() -> None:
    """
    Loads all active validators from node vitals
    :return: no return value
    """
    try:
        end_point_suffix = "/api/webmonitor/vitals"
        api_url = f"{Config.BASE_API_URI}{end_point_suffix}"
        result = get(api_url, timeout=15).json()
        validator_list = result['chain_view']['validator_view']
        ValidatorSet.load_validator_list(validator_list)
    except Exception as e:
        # TODO add proper logging + throw specific exception to break when called in a loop
        print(f"[{datetime.now()}]:{e}")
    return None


if __name__ == "__main__":
    ...
