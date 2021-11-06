import requests
import re
import os

# CLONING FUNCTIONS --------------------------------------------------------------------------------------------
def clone(url, user_agent):
    try:        
        u = url.replace('://', '-')
        q = 'templates/fake/{}'.format(u)
        os.makedirs(q, exist_ok=True)
        #os.system('wget -H -N -k -p -l 2 -nd -P {} --no-check-certificate -U "{}" {}'.format(q, user_agent, url))
        os.system('wget --no-check-certificate -O {}/index.html -c -k -U "{}" {}'.format(q, user_agent, url))
    except:
        pass
#--------------------------------------------------------------------------------------------------------------------