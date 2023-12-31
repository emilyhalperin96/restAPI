from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager 

from db import db

import models
import secrets

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resourses.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

#used for signing the JWTs 
#generate value, copy it, and use it as the secret key 
app.config['JWT_SECRET_KEY'] = secrets.SystemRandom().getrandbits(128)
jwt = JWTManager(app)

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

