from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, migrate as migrate_function, upgrade
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app
app = Flask(__name__)

# Your database configuration goes here
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app', 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def run_migrations():
    with app.app_context():
        # Check if migrations directory exists; if not, initialize migrations
        if not os.path.exists('migrations'):
            init(directory='migrations')
        
        # Prompt for a migration comment
        comment = input("Enter a comment for this migration: ")

        # Generate migration with dynamic comment
        migrate_function(directory='migrations', message=comment)

        # Apply migration
        upgrade(directory='migrations')

    print("Migration completed successfully!")

if __name__ == "__main__":
    run_migrations()