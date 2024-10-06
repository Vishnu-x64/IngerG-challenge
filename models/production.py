from db import db


class Production(db.Model):
    __tablename__ = 'production'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_well_number = db.Column(db.String, db.ForeignKey('well.api_well_number'), nullable=False)
    production_year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer, nullable=False)
    oil = db.Column(db.Float, nullable=False)
    gas = db.Column(db.Float, nullable=False)
    brine = db.Column(db.Float, nullable=False)
    days_operated = db.Column(db.Integer, nullable=False)
