from models import db, User
from werkzeug.security import generate_password_hash

admin = User(
    name="Admin",
    email="admin@pulse.com",
    phone="9999999999",
    password_hash=generate_password_hash("admin123"),
    role="admin"
)

db.session.add(admin)
db.session.commit()
exit()
