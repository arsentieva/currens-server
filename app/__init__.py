from flask import Flask
from flask_migrate import Migrate
from app.config import Configuration
from app.models import db
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

from app.routes.user import api as user
from app.routes.auth import api as auth
from app.routes.activities import api as activities


app = Flask(__name__)
CORS(app)


app.config.from_object(Configuration)
db.init_app(app)
jwt = JWTManager(app)

authorizations = {
    "token": {
        "type": "apiKey",
        "in":"header",
        "name": "Authorization",
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(app, authorizations=authorizations, security="token")
api.add_namespace(user)
api.add_namespace(auth)
api.add_namespace(activities)

migrate = Migrate(app, db)
