from app import db, app

with app.app_context():
    db.create_all()
    print("Database created!")

# This code creates the database and tables defined in the models.py file.
# It uses the SQLAlchemy ORM to create the database schema based on the models defined in the app.
