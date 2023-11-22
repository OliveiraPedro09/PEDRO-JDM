import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)


db = {
    'host':"localhost",
    'user':"root",
    'password':"Fatec!123",
    'database':"jdm",
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuario (nome, email) VALUES (%s, %s)", (nome, email))
        session['email'] = email
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('detalhes_usuario'))

    return render_template('cadastro.html')

@app.route('/detalhes')
def detalhes_usuario():
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor(dictionary=True)
    email = session['email']
    cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
    user = cursor.fetchone()

    print("DEBUG - Informações do usuário:", user)  

    return render_template('detalhes_usuario.html', user=user) 

@app.route('/logout', methods=['POST'])
def logout():
    if 'email' in session:
        session.pop('email', None)
        session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = '8f2bdd84d7c4443215a42c84dabd52b21f9bdd596790cd61'
    app.run(debug=True)