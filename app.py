from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura'
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

# Usuários e Tokens (Para exemplo, em produção use um método mais seguro!)
users = {
    "admin": generate_password_hash("secret")
}

# Simulação de um banco de dados de tokens
tokens = {
    "token123": "admin"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
    return None

# Definição do modelo de dados
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Livro {self.titulo}>'

# Rotas CRUD protegidas
@app.route('/livro', methods=['POST'])
@auth.login_required
def adicionar_livro():
    dados = request.json
    novo_livro = Livro(titulo=dados['titulo'], autor=dados['autor'])
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify({'mensagem': 'Livro adicionado com sucesso!'}), 201

# As outras rotas permanecem iguais, assegure-se de adicionar @auth.login_required para protegê-las

# Rota para login e geração de token
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    username = dados.get('username')
    password = dados.get('password')
    user_hash = users.get(username)
    if user_hash and check_password_hash(user_hash, password):
        # Gerar token, por simplicidade, estamos usando um token estático
        token = "token123"
        return jsonify({'token': token})
    return jsonify({'mensagem': 'Usuário ou senha inválidos'}), 401

# Executar o aplicativo
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria o banco de dados e as tabelas
    app.run(debug=True)
