from src import db
from src.api.oldata.models import AccountBalance
from src.api.connect import session

def get_acc_balances():
    return session.query(
        AccountBalance.id, 
        AccountBalance.address,
        AccountBalance.account_type,
        AccountBalance.balance,
        AccountBalance.updated_at)\
            .filter(AccountBalance.account_type=='community')\
            .all()
