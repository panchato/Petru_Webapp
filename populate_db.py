import logging
from app import app, db
from app.models import Client, Grower, Variety, RawMaterialPackaging

logging.basicConfig(level=logging.INFO)

def populate_models():
    with app.app_context():
        # Populating the Client model
        clients = [
            {"name": "Cliente A", "tax_id": "1234567890", "address": "123 Main St", "comuna": "Comuna1"},
            {"name": "Cliente B", "tax_id": "0987654321", "address": "456 Side St", "comuna": "Comuna2"}
        ]
        for client_data in clients:
            client = Client(**client_data)
            db.session.add(client)

        # Populating the Grower model
        growers = [
            {"name": "Productor A", "tax_id": "1111111111", "csg_code": "CSG1001"},
            {"name": "Productor B", "tax_id": "2222222222", "csg_code": "CSG1002"}
        ]
        for grower_data in growers:
            grower = Grower(**grower_data)
            db.session.add(grower)

        # Populating the Variety model
        varieties = [
            {"name": "Variedad A"},
            {"name": "Variedad B"}
        ]
        for variety_data in varieties:
            variety = Variety(**variety_data)
            db.session.add(variety)

        # Populating the RawMaterialPackaging model
        packagings = [
            {"name": "Bins Plásticos IFCO", "tare": 42.0},
            {"name": "Maxisaco Polipropileno", "tare": 2.5}
        ]
        for packaging_data in packagings:
            packaging = RawMaterialPackaging(**packaging_data)
            db.session.add(packaging)

        # Committing the session
        try:
            db.session.commit()
            logging.info("Data successfully added to the database.")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error occurred: {e}")

def setup_app():
    populate_models()

if __name__ == "__main__":
    setup_app()
