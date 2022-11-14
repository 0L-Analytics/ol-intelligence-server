from src import db
from src.api.oldata.models import AccountBalance
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

    data_py = session.query(
        AccountBalance.account_type,
        label("balance", cast(func.sum(AccountBalance.balance) / 1000000, Integer)),
        label("count", func.count(AccountBalance.id)))\
            .group_by(AccountBalance.account_type)\
            .order_by(AccountBalance.account_type)\
            .all()
    
    if data_py:
        balance_list = []
        count_list = []
        for obj in data_py:
            balance_list.append(obj[1])
            count_list.append(obj[2])
    
        out_py["data"] = data_py
        out_py["sum_balance"] = sum(balance_list)
        out_py["sum_count"] = sum(count_list)
    
    return out_py
