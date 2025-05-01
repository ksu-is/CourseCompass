from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

username = "testuser"
email = "test@example.com"
password = "testpass"

existing_user = User.query.filter_by(username=username).first()
if existing_user:
    print(f"User '{username}' already exists.")
else:
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    print(f"User '{username}' created successfully.")
