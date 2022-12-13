from flask_restx import Namespace, Resource, fields, reqparse

from src.api.ol_inputs import ol_address
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
    # @ol_namespace.expect(address, validate=True)
    @ol_namespace.response(200, "Success")
    @ol_namespace.response(400, "Error connecting to chain.")
    def get(self):
        """Returns a wallet type for an address"""
        # Define parser and request args
        request_parser = reqparse.RequestParser(bundle_errors=True)
        request_parser.add_argument('address', type=ol_address, required=True, location='args')
        args = request_parser.parse_args()

        """Returns wallet type."""
        wt = get_wallet_type(args['address'])
        if wt == "E":
            ol_namespace.abort(400, "Error connecting to chain.")

        return {'address': args['address'], 'wallet_type': wt}, 200


ol_namespace.add_resource(WalletType, "/wallettype")
