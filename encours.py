#!/usr/bin/python3

###Description: Permet de scanner le reseau d'un domaine et de parametrer les clients à distance"""

__author__ = "Delphine Demongeot"
__version__ = "1.0.0"
__email__ = "delphine.demongeot@gmail.com"
__status__ = "En cours de rédaction"

# Variables globales
fichiermdp = open("/root/.pwd" , "r")
pwd = /root/.pwd


import socket
import os

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
    print("Le PC " + ip + " est connecté \n")
    # Dépot de la clé publique sur le client
    cmd= ("sshpass -f /root/.pwd ssh-copy-id -i /root/.ssh/id_rsa.pub root@" + ip)