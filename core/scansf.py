import nmap
import requests

def nScan(ip):
    nm = nmap.PortScanner()
    nm.scan(ip, arguments="-F")
    for host in nm.all_hosts():
        ports = []
        protocols = []
        states = []
        for proto in nm[host].all_protocols():
            protocols.append(proto)
            lport = nm[host][proto].keys()
            for port in lport:
                ports.append(port)
                states.append(nm[host][proto][port]['state'])
        
        po = []
        for p in ports:
            n = {
            "Port": str(p),
            "Name": nm[host][proto][p]['name'],            
            "Reason": nm[host][proto][p]['reason'],
            "State": nm[host][proto][p]['state']
            }
            po.append(n)

        return po