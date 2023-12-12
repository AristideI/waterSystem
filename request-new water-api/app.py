from flask import Flask,jsonify
from flask_smorest import Api
from db import db
import os
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

from view.hob import blp as HobBlueprint
from view.branch import blp as BranchBlueprint
from view.cco import blp as CcoBlueprint
from view.cell import blp as CellBlueprint
from view.customer import blp as CustomerBlueprint
from view.district import blp as DistrictBlueprint
from view.sector import blp as SectorBlueprint
from view.wdo import blp as WDOBlueprint
from view.clientRequest import blp as ClientRequestBlueprint
from view.sendmail import blp as SendMailBlueprint
from view.cfo import blp as CFOaBlueprint
from view.poc import blp as POCBlueprint
from view.disconnect_pay import blp as DisconnectPayBlueprint


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "WASAC NEW WATER REQUEST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/wasac-rw"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] =os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    migrate=Migrate(app,db)

    api = Api(app)

    api.register_blueprint(HobBlueprint)
    api.register_blueprint(BranchBlueprint)
    api.register_blueprint(CcoBlueprint)
    api.register_blueprint(CellBlueprint)
    api.register_blueprint(CustomerBlueprint)
    api.register_blueprint(DistrictBlueprint)
    api.register_blueprint(SectorBlueprint)
    api.register_blueprint(WDOBlueprint)
    api.register_blueprint(ClientRequestBlueprint)
    api.register_blueprint(SendMailBlueprint)
    api.register_blueprint(CFOaBlueprint)
    api.register_blueprint(POCBlueprint)
    api.register_blueprint(DisconnectPayBlueprint)

    return app

