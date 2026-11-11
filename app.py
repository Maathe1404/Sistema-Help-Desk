from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta'

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['e-mail']
        password = request.form['password']
        flash ('Login efetuado com sucesso!')
        return redirect (url_for ('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

