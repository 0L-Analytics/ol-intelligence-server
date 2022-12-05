from flask import request
from flask_restx import Namespace, Resource, fields

from src.api.oldata.queries import (  # isort:skip
    get_acc_balances,
    get_balance_by_type,
)

oldata_namespace = Namespace("oldata")


acc_balance = oldata_namespace.model(
    "Account balance",
    {
        "id": fields.Integer(readOnly=True),
        "address": fields.String(required=True),
        "account_type": fields.String(required=True),
        "balance": fields.Integer(required=True),
        "updated_at": fields.DateTime,
    }
)

acc_balance_by_type = oldata_namespace.model(
    "Account balance by type",
    {
        "account_type": fields.String(required=True),
        "balance": fields.Integer(required=True),
    }
)


class AccountBalanceList(Resource):
    @oldata_namespace.marshal_with(acc_balance, as_list=True)
    def get(self):
        """Returns account balances."""
        return get_acc_balances(), 200


class AccountBalanceByType(Resource):
    @oldata_namespace.marshal_with(acc_balance_by_type, as_list=True)
    def get(self):
        """Returns account balances."""
        return get_balance_by_type(), 200


oldata_namespace.add_resource(AccountBalanceList, "/accountbalances")
oldata_namespace.add_resource(AccountBalanceByType, "/balancebytype")
