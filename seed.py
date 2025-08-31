from app import create_app, db
from app.models import Funcionario, Usuario

app = create_app()

dados = [
    ("Ana Souza","11111111111","ana@empresa.com","Av. A, 100","76870000","Ariquemes","RO"),
    ("Bruno Lima","22222222222","bruno@empresa.com","Rua B, 200","76870000","Ariquemes","RO"),
    ("Carla Reis","33333333333","carla@empresa.com","Rua C, 300","76870000","Ariquemes","RO"),
    ("Diego Alves","44444444444","diego@empresa.com","Rua D, 400","76870000","Ariquemes","RO"),
    ("Eva Melo","55555555555","eva@empresa.com","Rua E, 500","76870000","Ariquemes","RO"),
]

with app.app_context():
    db.create_all()
    if Funcionario.query.count() == 0:
        for nome, cpf, email, end, cep, cidade, estado in dados:
            f = Funcionario(nome_completo=nome, cpf=cpf, email=email,
                            endereco=end, cep=cep, cidade=cidade, estado=estado)
            u = Usuario(funcionario=f, username=email)
            u.set_password("123456")  # trocar em produção
            db.session.add_all([f, u])
        db.session.commit()
        print("Seed OK.")
    else:
        print("Já existem registros.")
