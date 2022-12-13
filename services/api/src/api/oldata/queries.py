from src import db
from src.api.oldata.models import (
    AccountBalance, 
    PaymentEvent, 
    AccountTransaction, 
    ActiveValidatorSet
)
from src.api.connect import session
from sqlalchemy.sql.expression import cast, func, label
from sqlalchemy import Integer


def get_acc_balances():
    return session.query(
        AccountBalance.id, 
        AccountBalance.address,
        AccountBalance.account_type,
        label("balance", cast(AccountBalance.balance / 1000000, Integer)),
        AccountBalance.updated_at)\
            .filter(AccountBalance.account_type=='community')\
            .all()


def get_acc_balance_by_type():
    out_py = {
        "data": [],
        "sum_balance": 0,
        "sum_count": 0,
    }

    acc_balances = session.query(
        AccountBalance.account_type,
        label("balance", cast(func.sum(AccountBalance.balance) / 1000000, Integer)),
        label("count", func.count(AccountBalance.id), Integer))\
            .group_by(AccountBalance.account_type)\
            .order_by(AccountBalance.account_type)\
            .all()
    
    acc_balance_sums = session.query(
        label("sum_balance", cast(func.sum(AccountBalance.balance) / 1000000, Integer)),
        label("sum_count", func.count(AccountBalance.id), Integer))\
            .first()
    
    out_py["data"] = acc_balances
    out_py["sum_balance"] = 0 if 'sum_balance' not in acc_balance_sums else int(acc_balance_sums['sum_balance'])
    out_py["sum_count"] = 0 if 'sum_count' not in acc_balance_sums else int(acc_balance_sums['sum_count'])
    
    return out_py


def get_payment_events_by_account(addr, seq_start, limit):
    return session.query(
        AccountTransaction.address,
        AccountTransaction.sequence_number,
        AccountTransaction.version,
        AccountTransaction.tx,
        AccountTransaction.hash,
        AccountTransaction.vm_status,
        AccountTransaction.gas_used,
        AccountTransaction.created_at)\
            .filter(
                AccountTransaction.address==addr, 
                AccountTransaction.sequence_number>=seq_start)\
            .order_by(AccountTransaction.sequence_number)\
            .limit(limit)\
            .all()


def get_active_validator_set():
    return session.query(
        ActiveValidatorSet.id,
        ActiveValidatorSet.address,
        ActiveValidatorSet.ip,
        ActiveValidatorSet._json,
        ActiveValidatorSet.last_active_epoch,
        ActiveValidatorSet.updated_at)\
            .filter(ActiveValidatorSet.is_active==True)\
            .all()
