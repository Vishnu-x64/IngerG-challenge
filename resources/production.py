from flask import Flask, request
from flask_smorest import Api, Blueprint, abort

from db import db
from models import Production
from schemas import ProductionResponse


blp = Blueprint('production', __name__)

@blp.route('/data')
@blp.response(200, ProductionResponse)
def get_production_data():
    well_number = request.args["well"]

    production_data = db.session.query(
        db.func.sum(Production.oil).label('oil'),
        db.func.sum(Production.gas).label('gas'),
        db.func.sum(Production.brine).label('brine')
    ).filter(Production.api_well_number==well_number).first()

    if production_data is None:
        abort(404, message="Well not found")

    return {
        "oil": production_data.oil,
        "gas": production_data.gas,
        "brine": production_data.brine
    }