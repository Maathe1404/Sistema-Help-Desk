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
                if usuario.tipo == 'solicitante':
                    return redirect (url_for('painel'))
                else:
                    return redirect (url_for('painel_suporte'))
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
        chamados = usuario_logado.chamados
        return render_template ('painel.html', usuario=usuario_logado, chamados=chamados)

@app.route('/painel_suporte', methods=['GET'])
def painel_suporte():
    if 'usuario_id' not in session:
        return redirect (url_for('login'))
    else:
        usuario_logado = Usuario.query.filter_by(id=session['usuario_id']).first()
        if usuario_logado is None or usuario_logado.tipo != 'suporte':
            return redirect(url_for('painel'))
        chamados = Chamado.query.all()
        return render_template ('painel_suporte.html', usuario=usuario_logado, chamados=chamados)

@app.route ('/atualizar_status/<int:id>', methods=['POST'])
def atualizar_status(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    else:
        usuario_logado = Usuario.query.filter_by(id=session['usuario_id']).first()
        if usuario_logado is None or usuario_logado.tipo != 'suporte':
            return redirect(url_for('painel'))
    chamado = Chamado.query.filter_by(id=id).first()
    if chamado is None:
        flash('Chamado não encontrado!')
        return redirect(url_for('painel_suporte'))
    novo_status = request.form['status']
    if novo_status not in ['aberto', 'em andamento', 'resolvido']:
        flash ('Status inválido!')
        return redirect(url_for('painel_suporte'))
    chamado.status = novo_status
    db.session.commit()
    flash('Status atualizado com sucesso!')
    return redirect(url_for('painel_suporte'))



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

@app.route('/novo_chamado', methods=['GET', 'POST'])
def novo_chamado():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form ['descricao']
        prioridade = request.form ['prioridade']
        novo_chamado = Chamado (
                    titulo = titulo,
                    descricao = descricao,
                    status = 'aberto',
                    prioridade = prioridade,
                    usuario_id = session['usuario_id']
                )
        db.session.add(novo_chamado)
        db.session.commit()
        flash('Chamado criado com sucesso!')
        return redirect(url_for ('painel'))
    return render_template ('novo_chamado.html')

with app.app_context():
    db.create_all()

    nome = 'Suporte 1'
    email = 'suporte1@helpdesk.com'
    senha = 'suporte123'
    senha_hash = generate_password_hash(senha)
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario is None:
        novo_usuario = Usuario (
            nome = nome,
            email = email,
            senha = senha_hash,
            tipo = 'suporte',
        )
        db.session.add(novo_usuario)
        db.session.commit()
        print('Usuario de suporte criado com sucesso!')
    else:
        print('Usuário de suporte já cadastrado!')

if __name__ == '__main__':
    app.run(debug=True)

