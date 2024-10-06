from flask import Flask, request
from flask_smorest import Api, Blueprint, abort

from db import db
from models import Production, Well
from schemas import ProductionResponse


blp = Blueprint('production', __name__)

@blp.route('/data')
@blp.response(200, ProductionResponse)
def get_production_data():
    well_number = request.args["well"]

    well = Well.query.get(well_number) 

    if well is None:
        abort(404, message="Well not found")

    annual_data = well.annual_production(2020)

    return {
        "oil": annual_data.total_oil,
        "gas": annual_data.total_gas,
        "brine": annual_data.total_brine
    }