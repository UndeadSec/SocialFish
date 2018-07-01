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

def pyNot():
    print(red("\n\n[!] Please use Python 3. $ python3 SocialFish.py "))

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
    print(red(" [!] Do you agree to use this tool for educational purposes only? (y/n) "))
    if input(cyan('\n SF > ')).upper() != 'Y':
        clear()
        print(red('\n[ YOU ARE NOT AUTHORIZED TO USE THIS TOOL ]\n'))
        exit(0)
