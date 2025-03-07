from flask import Flask, redirect, render_template, url_for, request, flash, session
from werkzeug.security import check_password_hash
from models.arbitro import Arbitro
from models.contratante import Contratante
from flask_login import LoginManager, login_user, login_required, logout_user
import mysql.connector

login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)

app.config['SECRET_KEY'] = 'muitodificil'


@login_manager.user_loader
def load_user(user_id):
    arbitro = Arbitro.get(int(user_id))
    if arbitro:
        return arbitro
    contratante = Contratante.get(int(user_id))
    return contratante


#primeira pagina (de abertura)
@app.route('/')
def inicial():
    return render_template('index.html')


#Pagina inicial (login)
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        arbitro = Arbitro.get_by_email(email)
        contratante = Contratante.get_by_email(email)
        if arbitro and check_password_hash(arbitro['arb_senha'], senha):
            # Guarda o tipo do usuário na sessão
            session['user_tipo'] = "arbitro"
            login_user(Arbitro.get(arbitro['arb_id']))
            return redirect(url_for('home'))

        elif contratante and check_password_hash(contratante['con_senha'], senha):
            # Guarda o tipo do usuário na sessão
            session['user_tipo'] = "contratante"
            login_user(Contratante.get(contratante['con_id']))
            return redirect(url_for('home'))
        
        else:
            flash("Email ou senha inválidos")
    return render_template('login.html')



#Pagina de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        senha = request.form['senha']
        conf_senha = request.form['confirmaSenha']
        tipo = request.form['tipo']

        if Arbitro.exists(email) or Contratante.exists(email):
            return "Email já cadastrado!", 400
        
        elif senha==conf_senha:
            if tipo == "arbitro":
                user = Arbitro(nome=nome, email=email, cpf=cpf, telefone=telefone, senha=senha)
                user.add_arbitro()            
                # logar o usuário após cadatro
                login_user(user)
                return redirect(url_for('login'))
            
            else:
                user = Contratante(nome=nome, email=email, cpf=cpf, telefone=telefone, senha=senha)
                user.add_contratante()            
                # logar o usuário após cadatro
                login_user(user)
                return redirect(url_for('login'))
            
        else:
            return "As senhas não são equivalentes"

    return render_template('login.html')


#Pagina principal (usuario)
@app.route('/home', methods=['GET', 'POST'])
@login_required 
def home():
    return render_template('home.html')


#Pagina sobre (informações)
@app.route('/sobre')
def sobre(): 
    return render_template('sobre.html')


#Pagina de solicitação (Cadastrar partidas)
@app.route('/solicitacao')
@login_required
def solicitacao():
    return render_template('solicitacao.html')


#Pagina onde ficará a galeria (fotos das partidas)
@app.route('/partidas')
@login_required
def partidas():
    return render_template('partidas.html')

#Pagina onde ficara a alteração de dados do usurio (editar)
@app.route('/configuracoes')
@login_required
def configuracoes():
    return render_template('configuracao.html')


#Pagina onde ficara as notificações do usuario
@app.route('/notificacoes')
@login_required
def notificacoes():
    return render_template('notificacoes.html')

@app.route('/saiba-mais')
def saiba_mais():
    return render_template('saiba_mais.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
