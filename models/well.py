import models

from sqlalchemy import func

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

    def annual_production(self, year):
        """Calculate annual production for the given year."""
        return db.session.query(
            func.sum(models.Production.oil).label('total_oil'),
            func.sum(models.Production.gas).label('total_gas'),
            func.sum(models.Production.brine).label('total_brine')
        ).filter(
            models.Production.api_well_number == self.api_well_number,
            models.Production.production_year == year
        ).first()