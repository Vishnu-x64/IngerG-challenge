import copy

import pandas as pd

from db import db
from models import Well, Production

def insert_well_data(wells_data):
    wells_data_copy = copy.deepcopy(wells_data)
    wells_data_copy.drop_duplicates(subset='API WELL  NUMBER', inplace=True)
    # Insert unique wells into the Wells table
    wells_records = []
    for _, row in wells_data_copy.iterrows():
        existing_well = Well.query.filter_by(api_well_number=row['API WELL  NUMBER']).first()
        if existing_well is None:
            well = Well(
                api_well_number=row['API WELL  NUMBER'],
                owner_name=row['OWNER NAME'],
                county=row['COUNTY'],
                township=row['TOWNSHIP'],
                well_name=row['WELL NAME'],
                well_number=row['WELL NUMBER']
            )
            wells_records.append(well)

    # Bulk insert wells data
    db.session.bulk_save_objects(wells_records)
    db.session.commit()


def insert_production_data(production_data):
    # Insert production data
    production_records = []
    for _, row in production_data.iterrows():
        existing_production = Production.query.filter_by(
            api_well_number=row['API WELL  NUMBER'],
            production_year=row['Production Year'],
            quarter=row['QUARTER 1,2,3,4']
        ).first()
        if existing_production is None:
            production = Production(
                api_well_number=row['API WELL  NUMBER'],
                production_year=row['Production Year'],
                quarter=row['QUARTER 1,2,3,4'],
                oil=row['OIL'],
                gas=row['GAS'],
                brine=row['BRINE'],
                days_operated=row['DAYS']
            )
            production_records.append(production)

    # Bulk insert production data
    db.session.bulk_save_objects(production_records)
    db.session.commit()

def load_data_to_db(data_file):
    data_types = {
        'API WELL  NUMBER': str,      # Keep as string if it has leading zeros
        'Production Year': int,
        'QUARTER 1,2,3,4': int,
        'OWNER NAME': str,
        'COUNTY': str,
        'TOWNSHIP': str,
        'WELL NAME': str,
        'WELL NUMBER': str,
        'OIL': float,                # Assuming it can be float
        'GAS': float,                # Assuming it can be float
        'BRINE': float,              # Assuming it can be float
        'DAYS': int
    }   
    data = pd.read_excel(data_file, dtype=data_types)
    insert_well_data(data[['API WELL  NUMBER', 'OWNER NAME', 'COUNTY', 'TOWNSHIP', 'WELL NAME', 'WELL NUMBER']].drop_duplicates())
    insert_production_data(data[['API WELL  NUMBER', 'Production Year', 'QUARTER 1,2,3,4', 'OIL', 'GAS', 'BRINE', 'DAYS']])


if __name__ == "__main__":
    load_data_to_db()
