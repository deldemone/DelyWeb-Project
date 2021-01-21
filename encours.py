#!/usr/bin/python3
# -*- coding: utf-8 -*-

###Description: Permet de scanner le reseau d'un domaine et de parametrer les clients à distance"""

__author__ = "Delphine Demongeot"
__version__ = "1.0.0"
__email__ = "delphine.demongeot@gmail.com"
__status__ = "En cours de rédaction"

#########################################################
####################  lES VARIABLES  ####################
#########################################################

DirWork = "/root/Work"
FicLOG = DirWork + "/debug.log"
fichiermdp = open("/root/.pwd" , "r")
FicInventaire = DirWork + "/invent.log"
retourfonction = ""

#########################################################
####################	lES MODULES  #################### 
#########################################################

import socket											# module communication réseau
import os												# module pour le système d'exploitation
import logging											# module de journalisation
import argparse 										# module d'analyse de ligne de commande
import random											# module génèration des nombres pseudo-aléatoires
from string import punctuation, ascii_letters, digits	# module des opérations usuelles sur les chaînes
import datetime					 						# Module format date & heure

#########################################################
#################### LES FONCTIONS ###################### 
#########################################################
#     Fonction "Génèration de chaîne aléatoire"
###

def aleatoireString(nbcar, type):
    # On détermine la complexité de la chaine à génèrer...
    alphanum = ascii_letters + digits
    symbols = alphanum + punctuation
    #...en fonction du type de chaine souhaité
    if (type == "REQ"):
            complexe = alphanum
            prefixe = type
    elif (type == "PWD"):
            complexe = symbols
            prefixe = ""
    # Génération de la chaine aléatoire avec le module random
    Str_aleatoire = random.SystemRandom()
    resultat = "".join(Str_aleatoire.choice(complexe) for i in range(nbcar))
    chaine_alea = prefixe + resultat
    return chaine_alea

# Exemple d'appel de fonction avec précision nb caractères et le type (REQ = Requête; PWD = Password; User)
# nbcar = 8  
# type = "REQ"  
# aleatoireString(nbcar, type)



#########################################################
########### JOURNALISATION & NIVEAU DE LOG ##############
#########################################################
#
# permet à l'utilisateur de nommer le niveau avec des majuscules ou des minuscules, 
# permet de spécifier un seul niveau et de choisir le niveau explicite dans un dictionnaire 
# avec pour valeur par défaut le niveau WARNING:
###
# Vérification de l'argument saisi lors de l'execution du script
parser = argparse.ArgumentParser()
parser.add_argument(
    "-log", 
    "--log", 
    default="warning",
    help=(
        "Préciser un niveau de journalisation."
        "Exemple --log debug', niveau par defaut ='warning'"),
    )
###
# Définition du namespace exemple : --log=INFO => Namespace(log='INFO')
options = parser.parse_args()
###
# Création du dictionnaire des niveaux de log
levels = {
    'critical': logging.CRITICAL,	# =50
    'error': logging.ERROR,			# =40
    'warn': logging.WARNING,		# =30
    'warning': logging.WARNING,		# =30
    'info': logging.INFO,			# =20
    'debug': logging.DEBUG			# =10
}
###
# Définir la correspondance niveau en numerique ex : debug=10 info=20
level = levels.get(options.log.lower())

###
# Condition si la syntaxe du niveau est erroné ou n'existe pas :
if level is None:
    raise ValueError(
        f"Niveau de log envoyé: {options.log}"
        f" -- devrait être : {' | '.join(levels.keys())}")
		
# Appel de la fonction de génération de chaîne aléatoire
nbcar = 5  
type = "REQ"  
retourfonction = aleatoireString(nbcar, type)
MSG = print("retour =" + str(retourfonction)) 

# Format de ligne de log
logging.basicConfig(filename=FicLOG, format='%(asctime)s ' + str(retourfonction) +' %(message)s', level=level)
   

#################### SCANNER d'IP #################### 
###
# Tableau qui stockera les ip connectées 
ipmachines = []
logging.info('Le scanner ip a démarré')
# Scan du réseau plage IP [1-254]
for ping in range(1,254):
    adresse = "192.168.122." + str(ping)
    socket.setdefaulttimeout(1)
# Récupération des informations
    try:
        hostname, alias, listadresse = socket.gethostbyaddr(adresse)
# Exception aucun client connecté avec IP
    except socket.herror:
        hostname = None
        alias = None
        listadresse = adresse
# On valorise le tableau avec les IP des PC connectés
    if (hostname != None):
        ipmachines.append(adresse)

#################### SESSION SSH #################### 		
# Connexion SSH vers les machines connectées
###
for ip in ipmachines:
    logging.info('Le PC ' + ip + ' est connecté')
    fichier = open(FicInventaire,"r")
    lignes = fichier.readlines()
    for ligne in lignes:
        if ip in ligne:
           MSG = "La clé du serveur est déja présente sur le client distant"
           print(MSG) 
           logging.info(MSG)
        else:
            fichier.close()
            fichier = open(FicInventaire,"a")
            print("clé pas dans l inventaire") 
            cmd= ("sshpass -f /root/.pwd ssh-copy-id -i /root/.ssh/id_rsa.pub root@" + ip)
            try:
                os.system(cmd)
                MSG = "Dépot de la clé publique sur le client"
                logging.info(MSG)
                now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                IN_INVENT = now + ";" + ip + ";"
                fichier.write("/n" + IN_INVENT)
                fichier.close()
            except:
                logging.error("LA clé n'a pas été déposé sur le client distant" + ip)

