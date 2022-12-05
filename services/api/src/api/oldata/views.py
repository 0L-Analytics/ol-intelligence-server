from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse

from src.api.oldata.ol_inputs import ol_address, int_range, natural
from src.api.oldata.queries import (  # isort:skip
    get_acc_balances,
    get_acc_balance_by_type,
    get_payment_events_by_account
)

oldata_namespace = Namespace("oldata")


acc_balance_full = oldata_namespace.model(
    "AccountBalanceFullModel",
    {
        "id": fields.Integer(readOnly=True),
        "address": fields.String(required=True),
        "account_type": fields.String(required=True),
        "balance": fields.Integer(required=True),
        "updated_at": fields.DateTime,
    }
)

acc_balance_core = oldata_namespace.model(
    "AccountBalanceCoreModel",
    {
        "address": fields.String(required=True),
        "account_type": fields.String(required=True),
        "balance": fields.Integer(required=True),
    }
)

acc_balance_by_type = oldata_namespace.model(
    "AccountBalanceByTypeModel",
    {
        "data": fields.List(fields.Nested(acc_balance_core)),
        "sum_balance": fields.Integer(required=True),
        "sum_count": fields.Integer(required=True),
    }
)

account_transaction_list = oldata_namespace.model(
    "AccountTransactionModel",
    {
        "address": fields.String(required=True),
        "sequence_number": fields.Integer(required=True),
        "version": fields.Integer(required=True),
        "tx": fields.Raw(required=True),
        "hash": fields.String(required=True),
        "vm_status": fields.String(required=True),
        "gas_used": fields.Integer(required=True),
        "created_at": fields.DateTime(required=True),
    }
)

class AccountBalanceList(Resource):
    @oldata_namespace.marshal_with(acc_balance_full, as_list=True)
    def get(self):
        """Returns account balances."""
        return get_acc_balances(), 200


class AccountBalanceByType(Resource):
    @oldata_namespace.marshal_with(acc_balance_by_type, as_list=False)
    def get(self):
        """Returns account balances."""
        return get_acc_balance_by_type(), 200


class AccountTransactionList(Resource):
    @oldata_namespace.marshal_with(account_transaction_list, as_list=True)
    def get(self):
        """Returns a list of transaction for a given account"""
        # Define parser and request args
        request_parser = reqparse.RequestParser(bundle_errors=True)
        request_parser.add_argument('address', type=ol_address, required=True, location='args')
        request_parser.add_argument('sequence', type=natural, default=0, required=False, location='args')
        request_parser.add_argument('limit', type=int_range(low=1, high=1000), default=100, required=False, location='args')
        # TODO Fix error parseArgs
        args = request_parser.parse_args()

        """Returns account balances."""
        return get_payment_events_by_account(args['address'], args['sequence'], args['limit']), 200


oldata_namespace.add_resource(AccountBalanceList, "/accountbalances")
oldata_namespace.add_resource(AccountBalanceByType, "/balancebytype")
oldata_namespace.add_resource(AccountTransactionList, "/account-transactions")
