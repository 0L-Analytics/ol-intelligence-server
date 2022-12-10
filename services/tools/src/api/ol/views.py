from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, reqparse

from src.api.ol_inputs import ol_address, int_range, natural
from src.api.ol.calls import (  # isort:skip
    get_wallet_type
)

ol_namespace = Namespace("ol")

address = ol_namespace.model(
    "address",
    {
        "address": fields.String(required=True),
    },
)

wallet_type = ol_namespace.clone(
    "Wallet type", 
    address, 
    {
        "wallet_type": fields.String(required=True),
    },
)


class WalletType(Resource):
    @ol_namespace.marshal_with(wallet_type)
    def get(self):
        """Returns a wallet type for an address"""
        # Define parser and request args
        request_parser = reqparse.RequestParser(bundle_errors=True)
        request_parser.add_argument('address', type=ol_address, required=True, location='args')
        args = request_parser.parse_args()

        """Returns wallet type."""
        return {"address": args['address'], 'wallet_type': ('S' if get_wallet_type(args['address']) else 'O')}, 200


# class WalletTypeList(Resource):
#     @ol_namespace.marshal_with(wallet_type, as_list=True)
#     def get(self):
#         """Returns a list of addresses with their wallet types"""
#         # Define parser and request args
#         request_parser = reqparse.RequestParser(bundle_errors=True)
#         request_parser.add_argument('address', type=ol_address, required=True, location='args')
#         request_parser.add_argument('sequence', type=natural, default=0, required=False, location='args')
#         request_parser.add_argument('limit', type=int_range(low=1, high=1000), default=100, required=False, location='args')
#         # TODO Fix error parseArgs
#         args = request_parser.parse_args()

#         """Returns account balances."""
#         return get_payment_events_by_account(args['address'], args['sequence'], args['limit']), 200


ol_namespace.add_resource(WalletType, "/wallettype")
# ol_namespace.add_resource(WalletTypeList, "/wallettypelist")
