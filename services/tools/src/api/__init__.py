from flask_restx import Api

from src.api.ping import ping_namespace
from src.api.ol.views import ol_namespace

api = Api(version="1.0", title="Users API", doc="/doc")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(ol_namespace, path="/ol")
