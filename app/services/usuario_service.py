from werkzeug.security import check_password_hash,generate_password_hash
from app.models.usuario import Usuario
from uuid import uuid1
from app.extensions import db

def check_usuario(username, password):
    user = Usuario.query.filter_by(usuario=username).first()
    if user and check_password_hash(user.senha, password):
        return user
    return None


def create_usuario(username, password):
    usuario_exist = Usuario.query.filter_by(usuario=username).first()

    if usuario_exist:
        return None

    new_usuario = Usuario(
        id=str(uuid1()),
        usuario=username,
        senha=generate_password_hash(password)
    )

    db.session.add(new_usuario)
    db.session.commit()

    return new_usuario