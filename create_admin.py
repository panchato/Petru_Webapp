import logging
from getpass import getpass
from app import app, db, bcrypt
from app.models import User

logging.basicConfig(level=logging.INFO)

def create_db():
    with app.app_context():
        db.create_all()
        logging.info("Database tables created.")

def create_admin_user():
    with app.app_context():
        admin_email = input("Enter admin email: ")
        admin_password = getpass("Enter admin password: ")
        password_hash = bcrypt.generate_password_hash(admin_password).decode('utf-8')
        if not User.query.filter_by(email=admin_email).first():
            admin_name = input("Enter admin name: ")
            admin_last_name = input("Enter admin last name: ")
            admin_phone = input("Enter admin phone number: ")
            admin_position = input("Enter admin position: ")

            admin = User(
                name=admin_name,
                last_name=admin_last_name,
                email=admin_email,
                phone_number=admin_phone,
                position=admin_position,
                is_active=True,
                user_type='admin',
                user_area='all',
            ) # type: ignore
            admin.password_hash = password_hash

            try:
                db.session.add(admin)
                db.session.commit()
                logging.info("Initial admin user added to the database.")
            except Exception as e:
                logging.error(f"Error adding admin user to the database: {e}")
        else:
            logging.info("Admin user already exists in the database.")

def setup_app():
    create_db()
    create_admin_user()

if __name__ == "__main__":
    setup_app()

