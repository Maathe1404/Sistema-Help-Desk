from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String (100), nullable=False)
    email = db.Column(db.String (120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String (20), nullable=False)
    chamados = db.relationship('Chamado', backref='usuario')

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    prioridade = db.Column(db.String(20), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['e-mail']
        password = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None:
            flash('E-mail não encontrado!')
        else:
            hash_verificacao = check_password_hash(usuario.senha, password)
            if hash_verificacao is True:
                flash ('Login efetuado com sucesso!')
                session['usuario_id'] = usuario.id
                return redirect (url_for('painel'))
            else:
                flash ('Senha inválida!')

        return redirect (url_for ('login'))

    return render_template('login.html')

@app.route('/painel', methods=['GET'])
def painel():
    if 'usuario_id' not in session:
        return redirect (url_for('login'))
    else:
        usuario_logado = Usuario.query.filter_by(id=session['usuario_id']).first()
        return render_template ('painel.html', usuario=usuario_logado)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['e-mail']
        password = request.form['password']
        senha_hash = generate_password_hash(password)
       
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente is None:
            novo_usuario = Usuario (
                        nome=nome,
                        email=email,
                        senha=senha_hash,
                        tipo='solicitante'
                    )
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!')
        else:
            flash('Este e-mail já esta cadastrado!')
        
    return render_template('cadastro.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect (url_for('login'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

