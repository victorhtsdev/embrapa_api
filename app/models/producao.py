from app.extensions import db

class Producao(db.Model):
    __tablename__ = 'producao'

    uuid = db.Column(db.String(36), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    control = db.Column(db.String(50))
    produto = db.Column(db.String(255))
    ano = db.Column(db.Integer,primary_key=True)
    quantidade = db.Column(db.Numeric(15, 2))
    tipo = db.Column(db.String(50))
    totalizador = db.Column(db.String(255))