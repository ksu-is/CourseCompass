from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Check if the user already exists
existing_user = User.query.filter_by(username='MMcGrath').first()

if existing_user:
    print("User 'MMcGrath' already exists.")
else:
    hashed_pw = generate_password_hash('KSU123')
    new_admin = User(
        username='MMcGrath',
        email='mmcgra13@students.kennesaw.edu',
        password=hashed_pw,
        is_admin=True
    )
    db.session.add(new_admin)
    db.session.commit()
    print("Admin user 'MMcGrath' created successfully.")
