from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class Funcionario(db.Model):
    __tablename__ = "funcionario"
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    endereco = db.Column(db.String(200))
    cep = db.Column(db.String(8))
    cidade = db.Column(db.String(80))
    estado = db.Column(db.String(2))
    usuario = db.relationship("Usuario", uselist=False, back_populates="funcionario", cascade="all, delete-orphan")

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionario.id", ondelete="CASCADE"), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)   # email ou cpf
    senha_hash = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    ultimo_login = db.Column(db.DateTime)

    funcionario = db.relationship("Funcionario", back_populates="usuario")
    log_acessos = db.relationship("LogAcesso", back_populates="usuario", cascade="all, delete-orphan")

    def set_password(self, senha: str):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class LogAcesso(db.Model):
    __tablename__ = "log_acesso"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip = db.Column(db.String(45))
    sucesso = db.Column(db.Boolean, nullable=False)
    motivo = db.Column(db.String(120))

    usuario = db.relationship("Usuario", back_populates="log_acessos")
