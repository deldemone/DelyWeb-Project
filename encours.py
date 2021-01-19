#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Description: Permet de scanner le reseau d'un domaine et de parametrer les clients à distance"""

__author__ = "Delphine Demongeot"
__version__ = "1.0.0"
__email__ = "delphine.demongeot@gmail.com"
__status__ = "En cours de rédaction"


import socket
from threading import Thread 
import queue

""" fonction appelé par le thread pour la recherche de l'hôte correspondant à une adresse """
""" IP donnée                                                                             """
""" Prend en argument l'adresse IP et l'instance de l'objet Queue créée dans le programme """
""" pricipal                                                                              """
def gethostname(address, q, hostnames):
    """ Gestion de l'exception au cas où un hôte ne répond pas à la demande """
    try:
        """ Appel de la fonction permettant de récupérer le nom d'hôte les alias """
        """    et les adresses IP de l'hôte                                      """
        hostname, alias, _ = socket.gethostbyaddr(address)
    except socket.herror:
       """ Aucun périphérique trouvé à l'adresse donnée en arguments """
        hostname = None
        alias = None
        addresslist = address
    """ On remplit le tableau avec les données récupérées """
    hostnames[address] = hostname
    """ On stocke le résultat dans l'objet Queue """

    q.put(hostnames)     

""" Programme princupal """
""" Création de l'objet Queue """
q = queue.Queue()
""" Tableau qui stockera les threads créés """
threads = []

""" dictionnaire stockant les noms d'hôte récupérés """ 
hostnames = {}

""" On défini la plage d'adresse IP à scruter """
for ping in range(1,254):
    """ Variable permettant de stocké l'adresse IP courante à scruter """
    address = "192.168.1." + str(ping)
    """ Création du thread avec appel de la fonction gethostname pour traitement de l'adresse IP """
    t = Thread(target=gethostname, args=(address,q, hostnames))

    """ On ajoute chaque thread dans le tableau """
    threads.append(t)

""" On démarre tous les threads créés """
for t in threads:
    t.start()
""" On unit tous les threads pour être sûr que tous ceux-ci renvoient leur valeur """
for t in threads:
    t.join()
""" On récupère les valeurs stockées dans la queue de threads et on les stocke dans le dictionnaire """
hostnames = q.get()
""" On itère chaque paire de clé/valeur à la recherche des noms d'hôte """
for address, hostname in hostnames.items():
    if (hostname != None):
        print(address, '=>', hostname)
        
 