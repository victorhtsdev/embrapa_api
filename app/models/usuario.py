from app.extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.String(36), primary_key=True)
    usuario = db.Column(db.String(80), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)