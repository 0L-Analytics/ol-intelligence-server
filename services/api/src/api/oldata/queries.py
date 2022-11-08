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


def get_balance_by_type():
    return session.query(
        AccountBalance.account_type,
        label("balance", cast(func.sum(AccountBalance.balance) / 1000000, Integer)))\
            .group_by(AccountBalance.account_type)\
            .all()