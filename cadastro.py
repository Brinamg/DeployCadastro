from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/youtube'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    sobrenome = db.Column(db.String(50))
    nacionalidade = db.Column(db.String(100))
    cep = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    logadouro = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "sobrenome": self.sobrenome,"nacionalidade": self.nacionalidade, "cep": self.cep,"estado": self.estado, "cidade": self.cidade, "logadouro": self.logadouro, "email": self.email, "telefone": self.telefone }


# Selecionar Tudo
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]

    return gera_response(200, "usuarios", usuarios_json)

# Selecionar Individual
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    return gera_response(200, "usuario", usuario_json)

# Cadastrar
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

    try:
        usuario = Usuario(nome=body["nome"], sobrenome=body["sobrenome"], nacionalidade=body["nacionalidade"],cep=body["cep"],estado=body["estado"], cidade=body["cidade"], logadouro=body["logadouro"], email=body["email"], telefone=body["telefone"])
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar")


# Atualizar
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_objeto.nome = body['nome']
        if('sobrenome' in body):
            usuario_objeto.nome = body['sobrenome']
        if('nacionalidade' in body):
            usuario_objeto.nome = body['nacionalidade']
        if('cep' in body):
            usuario_objeto.nome = body['cep']
        if('estado' in body):
            usuario_objeto.nome = body['estado']
        if('cidade' in body):
            usuario_objeto.nome = body['cidade']
        if('logadouro' in body):
            usuario_objeto.nome = body['logadouro']
        if('email' in body):
            usuario_objeto.email = body['email']
        if('telefone' in body):
            usuario_objeto.nome = body['telefone']
        
        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar")

# Deletar
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()