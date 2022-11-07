from flask_restx import Api

from src.api.auth import auth_namespace
from src.api.ping import ping_namespace
from src.api.users.views import users_namespace
from src.api.oldata.views import oldata_namespace

api = Api(version="1.0", title="Users API", doc="/doc")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(users_namespace, path="/users")
api.add_namespace(oldata_namespace, path="/oldata")
