from db import db


class Well(db.Model):
    __tablename__ = "well"

    api_well_number = db.Column(db.String, primary_key=True)
    owner_name = db.Column(db.String, nullable=False)
    county = db.Column(db.String, nullable=False)
    township = db.Column(db.String, nullable=False)
    well_name = db.Column(db.String, nullable=False)
    well_number = db.Column(db.String, nullable=False)

    production_info = db.relationship('Production', backref='well', lazy=True)