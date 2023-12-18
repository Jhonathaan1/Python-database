from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

def obter_conexao():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='72992982',
        database='pythonsql'
    )

def obter_usuario_por_email(email):
    try:
        with obter_conexao().cursor() as cursor:
            comando_verificacao = "SELECT * FROM venda WHERE email = %s"
            cursor.execute(comando_verificacao, (email,))
            usuario = cursor.fetchone()
            return usuario
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return None

def autenticar_usuario(email, senha):
    usuario = obter_usuario_por_email(email)
    if usuario and check_password_hash(usuario[2], senha):
        return True
    return False

def executar_sql(sql, valores=None):
    conexao = None
    try:
        conexao = obter_conexao()
        with conexao.cursor() as cursor:
            cursor.execute(sql, valores)
        conexao.commit()
    except mysql.connector.Error as err:
        print(f"Erro SQL: {err}")
    finally:
        if conexao:
            conexao.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('index2'))  # Redirecionar para index2 se o formulário for enviado
    else:
        return render_template('index.html')

@app.route('/cadastro.html')
def outra_pagina():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        if all(key in request.form for key in ['nome', 'email', 'senha']):
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']
            senha_hasheada = generate_password_hash(senha)

            comando = "INSERT INTO venda(nome, email, senha) VALUES (%s, %s, %s)"

            try:
                executar_sql(comando, (nome, email, senha_hasheada))
                flash('Cadastro realizado com sucesso! Faça o login.')
            except Exception as e:
                flash(f"Erro ao cadastrar usuário: {e}")

            return redirect(url_for('index'))
        else:
            flash('Erro no formulário. Verifique se todos os campos estão preenchidos.')

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha_digitada = request.form['senha']

        if autenticar_usuario(email, senha_digitada):
            session['email'] = email
            flash('Login bem-sucedido!')
            return redirect(url_for('index2'))  # Redirecionar para index2 após o login
        else:
            flash('E-mail ou senha incorretos. Tente novamente.')

    return render_template('index.html')

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)
