import os

from flask import Flask
from flask_smorest import Api

from resources.production import blp as ProductionBlueprint
from db import db
from pre_start import load_data_to_db


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "InerG REST API"
    app.config["API_VERSION"] = "InerG REST APIs"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inerg.db'

    db.init_app(app)

    api = Api(app=app)

    load_data = os.getenv("LOAD_DATA_FROM_FILE", 'False').lower() == 'true'
    
    with app.app_context():
        db.create_all()
        if load_data:
            load_data_to_db('data/20210309_2020_1 - 4 (1) (1) (1).xls')

    api.register_blueprint(ProductionBlueprint)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8080) 
