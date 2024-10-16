from app.extensions import db

class Exportacao(db.Model):
    __tablename__ = 'exportacao'

    uuid = db.Column(db.String(36), primary_key=True)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    object = db.Column(db.String(255))
    pais = db.Column(db.String(255))
    ano = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Numeric(15, 2))
    valor = db.Column(db.Numeric(15, 2))
