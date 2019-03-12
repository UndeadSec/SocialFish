import requests

# trace GEO IP -------------------------------------------------------------------------------------------------

def tracegeoIp(ip):    
    try:
        if '127.0.0.1' == ip:
            ip = 'https://geoip-db.com/json/'
        else:
            ip = 'https://geoip-db.com/jsonp/' + ip
        result = requests.get(ip).json()        
    except Exception as e:
        print(e)
        result = "Error. Verify your network connection."
    return result
# --------------------------------------------------------------------------------------------------------------