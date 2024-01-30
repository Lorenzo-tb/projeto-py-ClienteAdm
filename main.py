
from flask import Flask, jsonify, request, render_template, make_response, redirect, session
import urllib.parse

from flask_session import Session
import json
import random
from werkzeug.utils import secure_filename
import hashlib
import secrets
import psycopg2.extensions as ext
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models.usuario_model import ClienteAdm

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import requests

ext.string_types.pop(ext.JSON.values[0], None)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5433/alembic_db")
db_session = sessionmaker(bind=engine)()

# Configuração do Flask
app = Flask(__name__)
app.secret_key = '15fb15x15vb15f'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


class EmailSend:
    def __init__(self, smtp_port, smtp_server, email_sender, email_receiver, password):
        self.smtp_port = smtp_port
        self.smtp_server = smtp_server
        self.email_sender = email_sender
        self.email_receiver = email_receiver
        self.password = password

    def wellcome(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            msg['Subject'] = 'SEJA BEM VINDO'
            body = 'seja muito bem vindo ao nosso site'

            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_sender, self.password)
            text = msg.as_string()
            server.sendmail(self.email_sender, self.email_receiver, text)
            server.quit()
            print("Email enviado")
        except Exception as e:
            print("Erro: ", e)

    def password_email(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            msg['Subject'] = 'TROCA DE SENHA'

            body = 'A seguir o link para trocar sua senha:\
            <a href="http://localhost:5000/change_password">Trocar senha!</a>'

            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_sender, self.password)
            text = msg.as_string()
            server.sendmail(self.email_sender, self.email_receiver, text)
            server.quit()
            print("Email enviado")
        except Exception as e:
            print("Erro: ", e)

    def send_parabens(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            msg['Subject'] = 'FELIZ ANIVERSÁRIO'
            body = 'Os mais sinceros parabéns da nossa empresa, obrigado por ser esse cliente incrível'

            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_sender, self.password)
            text = msg.as_string()
            server.sendmail(self.email_sender, self.email_receiver, text)
            server.quit()
            print("Email enviado")
        except Exception as e:
            print("Erro: ", e)

    def send_fatores(self, senha_teste):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            msg['Subject'] = 'TESTE DE DOIS FATORES'
            
            body = 'Aqui esta o codigo para confirmar os dois fatores: ' + str(senha_teste)

            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_sender, self.password)
            text = msg.as_string()
            server.sendmail(self.email_sender, self.email_receiver, text)
            server.quit()
            print("Email enviado")
        except Exception as e:
            print("Erro: ", e)


# smtp_port = 587
# smtp_server = "email-ssl.com.br"
# email_sender = "informativo@selecao.vitoriasupervarejo.com.br"

def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    query = db_session.query(ClienteAdm).all()

    for user in query:
        if user.email == email:
            return False

    if re.search(regex, email):
        return True
    else:
        return False


def check_idade(nascimento):
    array_date = date.today().strftime("%Y-%m-%d").split("-")
    ano_date = int(array_date[0])
    mes_date = int(array_date[1])
    dia_date = int(array_date[2])

    nascimento_dividido = nascimento.split("-")
    ano = int(nascimento_dividido[0])
    mes = int(nascimento_dividido[1])
    dia = int(nascimento_dividido[2])

    idade = ano_date - ano
    if mes_date < mes:
        idade -= 1

    if mes_date == mes and dia_date < dia:
        idade -= 1

    return idade


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_session():
    try:
        if session['key'] and session['email'] and session['id']:
            return True
        else:
            return False
    except:
        return False


def check_cpf(cpf):
    if cpf == "000.000.000-00":
        return False

    aux = 10
    total = 0
    for numero in cpf:
        if aux == 1:
            break
        if numero != ".":
            print("aux: ", aux)
            print("numero: ", numero)
            mutiplicacao = int(numero) * aux
            total = total + mutiplicacao
            print(mutiplicacao)
            aux -= 1

    print(total)
    resto = total % 11
    if resto < 2 or resto == 10:
        primeiro_digito = 0
    else:
        primeiro_digito = 11 - resto

    total = 0
    aux = 11
    for numero in cpf:
        if aux == 2:
            print("aux: ", aux)
            print("numero: ", primeiro_digito)
            total = total + (int(primeiro_digito) * aux)
            print(total)
            break

        if numero != "." and numero != "-":
            print("aux: ", aux)
            print("numero: ", numero)
            mutiplicacao = int(numero) * aux
            total = total + mutiplicacao
            print(mutiplicacao)
            aux -= 1

    resto = total % 11
    print(resto)
    if resto < 2 or resto == 10:
        segundo_digito = 0
    else:
        segundo_digito = 11 - resto
    print(primeiro_digito, segundo_digito)
    print(cpf[12], cpf[13])

    if int(cpf[12]) == primeiro_digito and int(cpf[13]) == segundo_digito:
        return True
    else:
        return False


@app.route("/")
def home():
    if check_session():
        session['token'] = ""
        query = db_session.query(ClienteAdm).filter_by(
            id=session['id']).first()
        adm = query.adm
        print(adm)
        nascimento = query.nascimento
        print(nascimento)
        print(date.today())
        nascimento = nascimento.split('-')
        hoje = date.today().strftime("%Y-%m-%d").split("-")

        if nascimento[1] == hoje[1] and nascimento[2] == hoje[2]:
            aniversario = True
        else:
            aniversario = False

        print(aniversario)
        return render_template('users.html', adm=adm, aniversario=aniversario)
    else:
        return redirect("/login")


@app.route("/users")
def select_all():
    if check_session():
        query = db_session.query(ClienteAdm).all()
        nova_query = []
        hoje = date.today().strftime("%Y-%m-%d").split("-")

        for row in query:
            nascimento = row.nascimento
            nascimento = nascimento.split('-')

            if nascimento[1] == hoje[1] and nascimento[2] == hoje[2]:
                aniversario = True
            else:
                aniversario = False

            idade = check_idade(row.nascimento)
            nova_query.append({
                "id": row.id,
                "nome": row.nome,
                "nascimento": idade,
                "cpf": row.cpf,
                "genero": row.genero,
                "telefone": row.telefone,
                "foto": row.foto,
                "aniversario": aniversario,
                "bloqueado": row.bloqueado
            })
        print(nova_query)
        return make_response(jsonify(nova_query))
    else:
        return redirect("/login")


@app.route("/user_information/<int:id>")
def user_information(id=None):
    usuario = db_session.query(ClienteAdm).filter_by(id=id).first()
    print(usuario.adm)

    if usuario.adm:
        adm = "ADM"
    else:
        adm = "Cliente"

    return render_template('user.html', usuario=usuario, adm=adm)


@app.route("/login")
def login():
    session['token'] = ""
    session['key'] = ""
    session['email'] = ""
    session['id'] = ""
    session['fatores'] = ""
    return render_template('login.html')


@app.post("/do_login")
def do_login():
    email = request.form.get('email')
    senha = hashlib.sha256(request.form['senha'].encode()).hexdigest()
    query = db_session.query(ClienteAdm).filter_by(email=email).first()

    try:
        if secrets.compare_digest(senha, query.senha):
            if query.bloqueado:
                return make_response(jsonify({
                    "success": False,
                    "blocked": True,
                    "fatores": False
                }))
            else:
                if(query.fatores_email or query.telegram != ""):
                    return make_response(jsonify({
                        "success": False,
                        "blocked": False,
                        "fatores": True
                    }))
                else:
                    query.data_atualizacao = datetime.now()
                    db_session.commit()

                    before_hash = "{}{}{}".format(email, senha, datetime.now())
                    session['id'] = query.id
                    session['key'] = hashlib.sha256(before_hash.encode()).hexdigest()
                    session['email'] = email
                    return make_response(jsonify({
                        "success": True,
                    }))
        else:
            return make_response(jsonify({
                "success": False,
            }))
    except:
        return make_response(jsonify({
            "success": False,
        }))
    
@app.route("/login_fatores", methods = ["PUT", "GET"])
def login_fatores():
    if request.method == "PUT":
        tentativa = int(request.form['codigo'])
        email = request.form['email']
        senha = request.form['senha']
        senha = hashlib.sha256(request.form['senha'].encode()).hexdigest()
        print(tentativa)
        print(session['fatores'])
        if int(tentativa) == int(session['fatores']):
            usuario = db_session.query(ClienteAdm).filter_by(email=email).first()
            usuario.data_atualizacao = datetime.now()
            db_session.commit()
            before_hash = "{}{}{}".format(email, senha, datetime.now())
            session['id'] = usuario.id
            session['key'] = hashlib.sha256(before_hash.encode()).hexdigest()
            session['email'] = email
            return make_response(jsonify({
                "success": True,
            }))
        else:
            return make_response(jsonify({
                "success": False,
            }))
    else:
        email = request.args['email']
        usuario = db_session.query(ClienteAdm).filter_by(email=email).first()
        print(usuario)
        if usuario.fatores_email and usuario.telegram != "":
            try:
                smtp_port = 587
                smtp_server = "email-ssl.com.br"
                email_sender = "informativo@selecao.vitoriasupervarejo.com.br"
                password = '6A%X&#yNrv262B%4QVYxpR8*'
                email_receiver = email
                print(email_receiver)
                new_email = EmailSend(smtp_port, smtp_server, email_sender, email_receiver, password)
                senha_teste = random.randint(10000,99999)
                session['fatores'] = senha_teste
                new_email.send_fatores(senha_teste)

                chat = usuario.telegram
                token_bot = "5116553674:AAHBHlgK6BKPKReG2TUPqBwQG-HE7ic0uYo"
                message = f"Código de confirmação: {senha_teste}"
                message = urllib.parse.quote(message)
                url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&parse_mode=HTML&text={2}'.format(token_bot, chat, message)
                r = requests.get(url)
                
                return make_response(jsonify({
                    "success": True,
                }))
            except Exception as e:
                print(e)
                return make_response(jsonify({
                    "success": False,
                }))
        elif usuario.fatores_email and usuario.telegram == "":
            try:
                smtp_port = 587
                smtp_server = "email-ssl.com.br"
                email_sender = "informativo@selecao.vitoriasupervarejo.com.br"
                password = '6A%X&#yNrv262B%4QVYxpR8*'
                email_receiver = email
                print(email_receiver)
                new_email = EmailSend(smtp_port, smtp_server, email_sender, email_receiver, password)
                senha_teste = random.randint(10000,99999)
                session['fatores'] = senha_teste
                new_email.send_fatores(senha_teste)
                return make_response(jsonify({
                    "success": True,
                }))
            except Exception as e:
                print(e)
                return make_response(jsonify({
                    "success": False,
                }))
            
        elif not usuario.fatores_email and usuario.telegram != "":
            try:
                chat = usuario.telegram
                token_bot = "5116553674:AAHBHlgK6BKPKReG2TUPqBwQG-HE7ic0uYo"
                senha_teste = random.randint(10000,99999)
                session['fatores'] = senha_teste
                message = f"Código de confirmação: {senha_teste}"
                message = urllib.parse.quote(message)
                url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&parse_mode=HTML&text={2}'.format(token_bot, chat, message)
                r = requests.get(url)
                print(r)
                
                return make_response(jsonify({
                    "success": True,
                }))
            except Exception as e:
                print(e)
                return make_response(jsonify({
                    "success": False,
                }))
        else:
            return make_response(jsonify({
                "success": False,
            }))



@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['senha'] == request.form['confirme_senha']:
            nome = request.form['nome']
            email = request.form['email']
            senha = hashlib.sha256(request.form['senha'].encode()).hexdigest()
            nascimento = request.form['nascimento']
            cpf = request.form['cpf']
            genero = request.form['genero']
            telefone = request.form['telefone']
            foto = request.files['foto']
            filename = secure_filename(foto.filename)
            data_criacao = datetime.now()
            if filename != "":
                file_route = f'static/images/{filename}'
                foto.save(file_route)
                file_route = "../" + file_route
            else:
                file_route = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Foto-de-Perfil-en-WhatsApp-696x364.jpg/640px-Foto-de-Perfil-en-WhatsApp-696x364.jpg"

            if check_cpf(cpf):
                if check_email(email):
                    user = ClienteAdm(nome=nome, email=email, senha=senha, nascimento=nascimento, cpf=cpf, genero=genero, telefone=telefone, foto=file_route, data_criacao=data_criacao)
                    db_session.add(user)
                    db_session.commit()
                    smtp_port = 587
                    smtp_server = "email-ssl.com.br"
                    email_sender = "informativo@selecao.vitoriasupervarejo.com.br"
                    password = '6A%X&#yNrv262B%4QVYxpR8*'
                    email_receiver = email
                    new_email = EmailSend(smtp_port, smtp_server, email_sender, email_receiver, password)
                    senha_teste = random.randint(10000,99999)
                    session['fatores'] = senha_teste
                    new_email.send_fatores(senha_teste)

                    return make_response(jsonify({
                        "success": True,
                        "in_cpf": False,
                        "in_email": False,
                        "in_password": False
                    }))
                else:
                    return make_response(jsonify({
                        "success": False,
                        "in_cpf": False,
                        "in_email": True,
                        "in_password": False
                    }))
            else:
                return make_response(jsonify({
                    "success": False,
                    "in_cpf": True,
                    "in_email": False,
                    "in_password": False
                }))
        else:
            return make_response(jsonify({
                "success": False,
                "in_cpf": False,
                "in_email": False,
                "in_password": True
            }))
    else:
        session['token'] = ""
        session['key'] = ""
        session['email'] = ""
        session['id'] = ""
        return render_template("register.html")


@app.route('/perfil')
def perfil():
    if check_session():
        usuario = db_session.query(ClienteAdm).filter_by(id=session['id']).first()
        if usuario.adm:
            adm = "ADM"
        else:
            adm = "Cliente"

        print(adm)
        return render_template("perfil.html", usuario=usuario, adm=adm)
    else:
        return redirect("/login")
    

@app.put("/deactivate_fatores")
def deactivate_fatores():
    try:
        usuario = db_session.query(ClienteAdm).filter_by(id=session['id']).first()
        usuario.fatores_email = False
        usuario.telegram = ""
        db_session.commit()
        return make_response(jsonify({
            "success": True,
        }))
    except:
        return make_response(jsonify({
            "success": False,
        }))


@app.route('/email_fatores', methods = ["PUT", "GET"])
def email_fatores():

    if request.method == "PUT":
        tentativa = int(request.form['codigo'])
        print(tentativa)
        print(session['fatores'])
        if int(tentativa) == int(session['fatores']):
            usuario = db_session.query(ClienteAdm).filter_by(id=session['id']).first()
            usuario.fatores_email = True
            db_session.commit()
            return make_response(jsonify({
                "success": True,
            }))
        else:
            return make_response(jsonify({
                "success": False,
            }))
    else:
        try:
            smtp_port = 587
            smtp_server = "email-ssl.com.br"
            email_sender = "informativo@selecao.vitoriasupervarejo.com.br"
            password = '6A%X&#yNrv262B%4QVYxpR8*'
            email_receiver = session['email']
            print(email_receiver)
            new_email = EmailSend(smtp_port, smtp_server, email_sender, email_receiver, password)
            try:
                senha_teste = random.randint(10000,99999)
                session['fatores'] = senha_teste
                new_email.send_fatores(senha_teste)
            except:
                return make_response(jsonify({
                    "success": False,
                }))
                
            return make_response(jsonify({
                "success": True,
            }))
        except Exception as e:
            print(e)
            return make_response(jsonify({
                "success": False,
            }))

    
@app.route("/telegram_fatores", methods = ['PUT', 'POST'])
def telegram_fatores():
    if check_session():
        if request.method == 'PUT':
            id = request.form['id']
            codigo = request.form['codigo']
            if int(codigo) == int(session['fatores']):
                try:
                    query = db_session.query(ClienteAdm).filter_by(id=id).first()
                    db_session.commit()
                    return make_response(jsonify({
                        "success": True,
                    }))
                except Exception as e:
                    print(e)
                    return make_response(jsonify({
                        "success": False,
                    }))
            else:
                return make_response(jsonify({
                    "success": False,
                }))
            
        else:
            try:
                id = request.form['id']
                telegram = request.form['telegram']
                db_session.commit()
                chat = telegram
                token_bot = "5116553674:AAHBHlgK6BKPKReG2TUPqBwQG-HE7ic0uYo"
                codigo = random.randint(10000, 99999)
                session['fatores'] = codigo
                message = f"Código de confirmação: {codigo}"
                print(chat)
                print(codigo)
                print(message)
                message = urllib.parse.quote(message)
                url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&parse_mode=HTML&text={2}'.format(token_bot, chat, message)
                print(url)
                r = requests.get(url)
                print(r.json())
                if r.status_code == 200:
                    query = db_session.query(ClienteAdm).filter_by(id=id).first()
                    query.telegram = telegram
                    
                    db_session.commit()
                    return make_response(jsonify({
                        "success": True,
                    }))
                else:
                    return make_response(jsonify({
                        "success": False,
                    }))
                
            except Exception as e:
                print(e)
                return make_response(jsonify({
                    "success": False,
                }))
    else:
        return redirect("/login")
    

@app.route("/login_telegram", methods = ["PUT", "GET"])
def login_telegram():
    email = session['email']
    query = db_session.query(ClienteAdm).filter_by(email=email).first()
    chat = query.telegram
    token_bot = "5116553674:AAHBHlgK6BKPKReG2TUPqBwQG-HE7ic0uYo"
    codigo = random.randint(10000, 99999)
    session['fatores'] = codigo
    message = f"Código de confirmação: {codigo}"
    print(chat)
    print(codigo)
    print(message)
    message = urllib.parse.quote(message)
    url = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&parse_mode=HTML&text={2}'.format(token_bot, chat, message)
    print(url)
    r = requests.get(url)
    print(r.json())
    if r.status_code == 200:        
        db_session.commit()
        return make_response(jsonify({
            "success": True,
        }))
    else:
        return make_response(jsonify({
            "success": False,
        }))




@app.route("/update_user/<int:id>", methods=['PUT', 'GET'])
def update(id=None):
    if check_session():
        if request.method == 'PUT':
            nome = request.form['nome']
            nascimento = request.form['nascimento']
            cpf = request.form['cpf']
            genero = request.form['genero']
            telefone = request.form['telefone']
            foto = request.files['foto']
            filename = secure_filename(foto.filename)
            query = db_session.query(ClienteAdm).filter_by(id=id).first()
            adm = request.form['adm']

            adm = False if adm == 'cliente' else True

            if filename != "":
                file_route = f'static/images/{filename}'
                foto.save(file_route)
                file_route = "../" + file_route
            else:
                file_route = query.foto

            if check_cpf(cpf):
                try:
                    query.nome = nome
                    query.nascimento = nascimento
                    query.cpf = cpf
                    query.genero = genero
                    query.telefone = telefone
                    query.foto = file_route
                    query.adm = adm
                    db_session.commit()
                    return make_response(jsonify({
                        "success": True,
                    }))
                except:
                    return make_response(jsonify({
                        "success": False
                    }))
            else:
                return make_response(jsonify({
                    "success": False
                }))
        else:
            query = db_session.query(ClienteAdm).filter_by(id=id).first()

            id = query.id
            nome = query.nome
            nascimento = query.nascimento
            cpf = query.cpf
            genero = query.genero
            telefone = query.telefone
            foto = query.foto
            return render_template('update_user.html', id=id, nome=nome, nascimento=nascimento, cpf=cpf, genero=genero, telefone=telefone, foto=foto)
    else:
        return redirect("/login")


@app.put("/update_image")
def update_image():
    if check_session():
        id = request.form['id']
        foto = request.files['foto']
        filename = secure_filename(foto.filename)
        file_route = f'static/images/{filename}'
        foto.save(file_route)
        file_route = "../" + file_route
        query = db_session.query(ClienteAdm).filter_by(id=id).first()
        try:
            query.foto = file_route
            db_session.commit()
            return make_response(jsonify({
                "success": True,
            }))
        except:
            return make_response(jsonify({
                "success": False
            }))
    else:
        return redirect("/login")


@app.delete("/delete_user/<int:id>")
def delete(id=None):
    if check_session():
        try:
            query = db_session.query(ClienteAdm).filter_by(id=id).first()
            db_session.delete(query)
            db_session.commit()
            return make_response(jsonify({
                "success": True,
            }))
        except:
            return make_response(jsonify({
                "success": False
            }))
    else:
        return redirect("/login")


@app.delete("/delete_more")
def delete_more():
    if check_session():
        pessoas = json.loads(request.form.get("selecionados"))
        print(pessoas)
        try:
            for pessoa in pessoas:
                query = db_session.query(
                    ClienteAdm).filter_by(id=pessoa).first()
                db_session.delete(query)
                db_session.commit()
            return make_response(jsonify({
                "success": True,
            }))
        except:
            return make_response(jsonify({
                "success": False
            }))
    else:
        return redirect("/login")


@app.put("/block_user/<int:id>")
def block_user(id=None):
    if check_session():
        try:
            query = db_session.query(ClienteAdm).filter_by(id=id).first()
            query.bloqueado = True
            db_session.commit()
            return make_response(jsonify({
                "success": True,
            }))
        except:
            return make_response(jsonify({
                "success": False
            }))
    else:
        return redirect("/login")


@app.put("/unblock_user/<int:id>")
def unblock_user(id=None):
    if check_session():
        try:
            query = db_session.query(ClienteAdm).filter_by(id=id).first()
            query.bloqueado = False
            db_session.commit()
            return make_response(jsonify({
                "success": True,
            }))
        except:
            return make_response(jsonify({
                "success": False
            }))
    else:
        return redirect("/login")


@app.route("/forgot_password")
def forgot_password():
    try:
        print(request.args['email'])
        email = request.args['email']
        print(email)
        smtp_port = 587
        smtp_server = "email-ssl.com.br"
        email_sender = "informativo@selecao.vitoriasupervarejo.com.br"
        password = '6A%X&#yNrv262B%4QVYxpR8*'

        new_email = EmailSend(smtp_port, smtp_server, email_sender, email, password)
        session['email'] = email
        before_hash = "{}{}".format(email, datetime.now())

        session['token'] = hashlib.sha256(before_hash.encode()).hexdigest()
        new_email.password_email()

        return make_response(jsonify({
            "success": True
        }))
    except Exception as e:
        print(e)
        return make_response(jsonify({
            "success": False
        }))


@app.route("/change_password", methods=['POST', 'GET'])
def change_password():
    if request.method == 'POST':
        if request.form['senha'] == request.form['confirm_senha']:
            try:
                query = db_session.query(ClienteAdm).filter_by(
                    email=session['email']).first()
                senha = hashlib.sha256(
                    request.form['senha'].encode()).hexdigest()
                query.senha = senha
                db_session.commit()
                return make_response(jsonify({
                    "success": True,
                    "in_password": False
                }))
            except Exception as e:
                return make_response(jsonify({
                    "success": False,
                    "in_password": False
                }))
        else:
            return make_response(jsonify({
                "success": False,
                "in_password": True
            }))
    else:
        if session['token'] != "":
            return render_template('change_password.html')
        else:
            return {
                "message": "sem permissao"
            }


@app.route("/dash_boards")
def dash_boards():
    datas = []
    homens = []
    mulheres = []
    dia = int(date.today().strftime("%d").split("-")[0])
    mes = int(date.today().strftime("%m").split("-")[0])
    ano = int(date.today().strftime("%y").split("-")[0])
    print(dia)
    print(mes)
    print(ano)
    data_atual = datetime.now()

    for i in range(7):

        data_desejada = data_atual - timedelta(days=i)
        hoje = f"{ano}-{mes:02d}-{dia:02d}"

        query_homem = db_session.query(func.date(ClienteAdm.data_atualizacao).label('data'), func.count('*').label('total_pessoas')).filter(
            ClienteAdm.genero == "masculino", func.date(ClienteAdm.data_atualizacao) == data_desejada.date()).group_by(func.date(ClienteAdm.data_atualizacao)).first()
        if query_homem:
            homens.append(query_homem.total_pessoas)
        else:
            homens.append(0)

        query_total = db_session.query(func.date(ClienteAdm.data_atualizacao).label('data'), func.count('*').label('total_pessoas')).filter(
            ClienteAdm.genero == "feminino", func.date(ClienteAdm.data_atualizacao) == data_desejada.date()).group_by(func.date(ClienteAdm.data_atualizacao)).first()
        if query_total:
            mulheres.append(query_total.total_pessoas)
        else:
            mulheres.append(0)
        datas.append(hoje)
        dia -= 1
    print(datas)
    print(homens)
    print(mulheres)
    print(datas)

    aniversariantes = []
    query = db_session.query(ClienteAdm).all()
    for pessoa in query:
        nascimento = pessoa.nascimento.split('-')
        hoje = date.today().strftime("%Y-%m-%d").split("-")
        if nascimento[1] == hoje[1] and nascimento[2] == hoje[2]:
            aniversariantes.append(pessoa)
        else:
            aniversario = False

    quan_telefones = db_session.query(func.count(ClienteAdm.id)).filter(
        ClienteAdm.telefone != "").scalar()
    quan_pessoas = db_session.query(func.count(ClienteAdm.id)).scalar()
    quan_sem_tel = quan_pessoas - quan_telefones
    print(quan_pessoas)
    print(quan_telefones)
    datas.reverse()
    homens.reverse()
    mulheres.reverse()
    query = db_session.query(ClienteAdm).filter_by(id=session['id']).first()
    adm = query.adm
    return render_template("dash_board.html", datas=datas, homens=homens, mulheres=mulheres, quan_telefones=quan_telefones, quan_sem_tel=quan_sem_tel, adm=adm)


@app.route("/aniversariantes")
def aniversariantes():
    aniversariantes = []
    query = db_session.query(ClienteAdm).all()
    for pessoa in query:
        nascimento = pessoa.nascimento.split('-')
        hoje = date.today().strftime("%Y-%m-%d").split("-")
        if nascimento[1] == hoje[1] and nascimento[2] == hoje[2]:
            idade = check_idade(pessoa.nascimento)
            aniversariantes.append({
                "id": pessoa.id,
                "nome": pessoa.nome,
                "nascimento": idade,
                "cpf": pessoa.cpf,
                "genero": pessoa.genero,
                "telefone": pessoa.telefone,
                "foto": pessoa.foto,
                "bloqueado": pessoa.bloqueado
            })

    return make_response(jsonify(aniversariantes))


@app.route("/feliz_aniversario/<int:id>")
def feliz_aniversario(id=None):
    try:
        print(id)
        email = db_session.query(ClienteAdm.email).filter_by(id=id).first()
        print(email[0])
        smtp_port = 587
        smtp_server = "email-ssl.com.br"
        email_sender = "informativo@selecao.vitoriasupervarejo.com.br"
        password = '6A%X&#yNrv262B%4QVYxpR8*'
        new_email = EmailSend(smtp_port, smtp_server, email_sender, email[0], password)
        new_email.send_parabens()

        return make_response(jsonify({
            "success": True
        }))
    except Exception as e:
        print(e)
        return make_response(jsonify({
            "success": False
        }))
