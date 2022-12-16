from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse

from src.api.oldata.ol_inputs import ol_address, int_range, natural
from src.api.oldata.queries import (  # isort:skip
    get_acc_balances,
    get_acc_balance_by_type,
    get_payment_events_by_account,
    get_active_validator_set,
    get_tokenomics,
    get_supply_liquidity,
    get_addr_bal_distribution,
    get_top_addr_distribution,
    get_top_100_distribution
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

acc_bal_by_type = oldata_namespace.model(
    "AccountBalanceByTypeModel",
    {
        "account_type": fields.String(required=True),
        "balance": fields.Integer(required=True),
        "count": fields.Integer(required=True),
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

validator_set = oldata_namespace.model(
    "ValidatorSet",
    {
        "id": fields.Integer(readOnly=True),
        "address": fields.String(required=True),
        "ip": fields.String(required=True),
        "_json": fields.Raw(required=True),
        "tower_epoch": fields.Integer(required=True),
        "updated_at": fields.DateTime(required=True),
    }
)

tokenomics_single_measures = oldata_namespace.model(
    "TokenomicsSingleMeasures",
    {
        "total_balance": fields.Integer(required=True),
        "total_addr_cnt": fields.Integer(required=True),
        "top10_balance": fields.Integer(required=True),
        "top100_balance": fields.Integer(required=True),
        "top10_balance_nv": fields.Integer(required=True),
        "top10_perc": fields.Float(required=True),
        "top100_perc": fields.Float(required=True),
        "top10_nv_perc": fields.Float(required=True),
        "sum_bal_ex_com": fields.Integer(required=True),
        "sum_bal_ex_com_val": fields.Integer(required=True),
        "addr_cnt_bal_gt1": fields.Integer(required=True),
        "bal_community": fields.Integer(required=True),
        "bal_slow": fields.Integer(required=True),
        "bal_liquid": fields.Integer(required=True),
        "cnt_community": fields.Integer(required=True),
        "cnt_slow": fields.Integer(required=True),
        "cnt_liquid": fields.Integer(required=True),
        "active_set_cnt": fields.Integer(required=True),
        "validator_cnt": fields.Integer(required=True)
    }
)

supply_liquidity  = oldata_namespace.model(
    "SupplyLiquidityModel",
    {
        "wallet_type_name": fields.String(required=True),
        "balance": fields.Integer(required=True),
        "count": fields.Integer(required=True),
    }
)

address_balance_distrib = oldata_namespace.model(
    "AddressBalanceDistributionModel",
    {
        "balance": fields.Integer(required=True),
        "bucket_name": fields.String(required=True),
        "bucket_order": fields.Integer(required=True),
    }
)

top_addr_distrib = oldata_namespace.model(
    "TopAddressDistributionModel",
    {
        "bucket_name": fields.String(required=True),
        "balance_perc": fields.Float(required=True),
        "bucket_cumul": fields.Integer(required=True),
        "bucket_order": fields.Integer(required=True),
    }
)

top_100_distrib = oldata_namespace.model(
    "Top100DistributionModel",
    {
        "balance": fields.Integer(required=True),
        "addr_order": fields.Integer(required=True),
    }
)


class AccountBalanceList(Resource):
    @oldata_namespace.marshal_with(acc_balance_full, as_list=True)
    def get(self):
        """Returns account balances."""
        return get_acc_balances(), 200


class AccountBalanceByType(Resource):
    @oldata_namespace.marshal_with(acc_bal_by_type, as_list=False)
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


class ActiveValidatorSet(Resource):
    @oldata_namespace.marshal_with(validator_set, as_list=True)
    def get(self):
        """Returns account balances."""
        return get_active_validator_set(), 200


class TokenomicsSingleMeasures(Resource):
    @oldata_namespace.marshal_with(tokenomics_single_measures, as_list=False)
    def get(self):
        """Returns tokenomics."""
        return get_tokenomics(), 200


class SupplyLiquidity(Resource):
    @oldata_namespace.marshal_with(supply_liquidity, as_list=True)
    def get(self):
        """Returns supply liquidity."""
        return get_supply_liquidity(), 200


class AddressBalanceDistribution(Resource):
    @oldata_namespace.marshal_with(address_balance_distrib, as_list=True)
    def get(self):
        """Returns balance distribution by address."""
        return get_addr_bal_distribution(), 200


class TopAddressDistribution(Resource):
    @oldata_namespace.marshal_with(top_addr_distrib, as_list=True)
    def get(self):
        """Returns balance distribution by top addresses."""
        return get_top_addr_distribution(), 200


class Top100Distribution(Resource):
    @oldata_namespace.marshal_with(top_100_distrib, as_list=True)
    def get(self):
        """Returns balance distribution by top addresses."""
        return get_top_100_distribution(), 200


oldata_namespace.add_resource(AccountBalanceList, "/accountbalances")
oldata_namespace.add_resource(AccountBalanceByType, "/balancebytype")
oldata_namespace.add_resource(AccountTransactionList, "/accounttransactions")
oldata_namespace.add_resource(ActiveValidatorSet, "/activeset")
oldata_namespace.add_resource(TokenomicsSingleMeasures, "/tokenomics")
oldata_namespace.add_resource(SupplyLiquidity, "/supplyliquidity")
oldata_namespace.add_resource(AddressBalanceDistribution, "/addrbaldistribution")
oldata_namespace.add_resource(TopAddressDistribution, "/topaddrbaldistribution")
oldata_namespace.add_resource(Top100Distribution, "/top100distribution")
