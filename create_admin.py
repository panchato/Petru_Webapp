import logging
from getpass import getpass
from app import app, db, bcrypt
from app.models import User, Role

logging.basicConfig(level=logging.INFO)

def create_db():
    with app.app_context():
        db.create_all()
        logging.info("Database tables created.")

def create_admin_user():
    with app.app_context():
        admin_email = input("Enter admin email: ")
        admin_user = User.query.filter_by(email=admin_email).first()

        if admin_user is None:
            admin_password = getpass("Enter admin password: ")
            password_hash = bcrypt.generate_password_hash(admin_password).decode('utf8')
            admin_name = input("Enter admin name: ")
            admin_last_name = input("Enter admin last name: ")
            admin_phone = input("Enter admin phone number: ")

            admin_user = User(
                name=admin_name,
                last_name=admin_last_name,
                email=admin_email,
                phone_number=admin_phone,
                is_active=True,
                is_external=False,
                password_hash=password_hash
            ) # type: ignore
            db.session.add(admin_user)
            try:
                db.session.commit()
                logging.info("Initial admin user added to the database.")
            except Exception as e:
                logging.error(f"Error adding admin user to the database: {e}")
                db.session.rollback()
                return  # Exit the function if the user can't be added

        admin_role = Role.query.filter_by(name='Admin').first()
        if admin_role is None:
            admin_role = Role(name='Admin', description='Líder Supremo') # type: ignore
            db.session.add(admin_role)
            db.session.commit()

        # Refresh admin_user to ensure it's not None after insertion
        admin_user = User.query.filter_by(email=admin_email).first()
        if admin_user and admin_role not in admin_user.roles:
            admin_user.roles.append(admin_role)
            try:
                db.session.commit()
            except Exception as e:
                logging.error(f"Error linking admin user to role: {e}")
                db.session.rollback()

def setup_app():
    create_db()
    create_admin_user()

if __name__ == "__main__":
    setup_app()
