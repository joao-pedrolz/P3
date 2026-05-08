from flask_login import UserMixin
from .database import db

def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Livro(db.Model):
    __tablename__ = "livros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
        }

class Propriedades(db.Model):
    __tablename__ = "propriedades"

    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey("livros.id"), nullable=False)
    atributo = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "livro_id": self.livro_id,
            "atributo": self.atributo,
            "valor": self.valor
        }

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    senha = db.Column(db.String(200), nullable=False)