#!/usr/bin/python3
# -*- coding: utf-8 -*-

###Description: Permet de scanner le reseau d'un domaine et de parametrer les clients à distance"""

__author__ = "Delphine Demongeot"
__version__ = "1.0.0"
__email__ = "delphine.demongeot@gmail.com"
__status__ = "En cours de rédaction"

# Variables globales
fichiermdp = open("/root/.pwd" , "r")
chaine_alea = ""

import socket
import os
import logging
import random

from string import punctuation, ascii_letters, digits


def aleatoireString(nbcar, type):
    symbols = ascii_letters + digits
    Str_aleatoire = random.SystemRandom()
    password = "".join(Str_aleatoire.choice(symbols) for i in range(nbcar))
    chaine_alea = type + password
    print("STRING=" + chaine_alea)


	
	
# Log : DEBUG
def log(chaine_alea):
logging.basicConfig(filename='test_log.log',level=logging.DEBUG,\
      format='%(asctime)s -- ' + chaine_alea + ' -- %(levelname)s -- %(message)s')
	  
# logger.debug('Information Debug')
# logger.info('Information Info')
# logger.warning('Avertissement')
# logger.error('Message d’erreur')
# logger.critical('Erreur grave')

# Tableau qui stockera les ip connectées """
ipmachines = []
logger.info('Le scanner ip a démarré')
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
    nbcar = 8  
    type = "REQ"  
    aleatoireString(nbcar, type)
    log(chaine_alea)
    logger.info(chainealea + "Le PC " + ip + " est connecté")
    # Dépot de la clé publique sur le client
    cmd= ("sshpass -f /root/.pwd ssh-copy-id -i /root/.ssh/id_rsa.pub root@" + ip)
    os.system(cmd)