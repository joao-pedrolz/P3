from livrosp3 import create_app
from livrosp3.database import db

app = create_app()

with app.app_context():
    db.create_all()