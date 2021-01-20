###Description: Permet de scanner le reseau d'un domaine et de parametrer les clients à distance"""

__author__ = "Delphine Demongeot"
__version__ = "1.0.0"
__email__ = "delphine.demongeot@gmail.com"
__status__ = "En cours de rédaction"

# Variables globales
fichiermdp = open('/root/.pwd')
pwd = fichiermdp.read()
username = "root"

import socket
import paramiko

# Tableau qui stockera les ip connectées """
ipmachines = []


for ping in range(1,254):
    adresse = "192.168.122." + str(ping)
    socket.setdefaulttimeout(1)

    try:
        hostname, alias, listadresse = socket.gethostbyaddr(adresse)

    except socket.herror:
        hostname = None
        alias = None
        listadresse = adresse

    if (hostname != None):
        ipmachines.append(adresse)
		
# Connexion SSH vers les machines connectées
for ip in ipmachines:
    print(ip)
    print(pwd)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, 22, username, pwd)
    stdin, stdout, stderr = ssh.exec_command(ls)

    lines = stdout.readlines()

    print(lines)
    client.close()



	