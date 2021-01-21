#!/usr/bin/python3
# -*- coding: utf-8 -*-

###Description: Permet de scanner le reseau d'un domaine et de parametrer les clients à distance"""
##################################################################################################################
__author__ = "Delphine Durand Demongeot"
__version__ = "1.0.0"
__email__ = "dd0275416@gmail.com"
__status__ = "En cours de rédaction"


##################################################################################################################
#	LES MODULES
#=======================================================#

import socket		# module communication réseau
import os			# module pour le système d'exploitation
import logging		# module de journalisation
import argparse 	# module d'analyse de ligne de commande
import random		# module génèration des nombres pseudo-aléatoires
from string import punctuation, ascii_letters, digits	# module des opérations usuelles sur les chaînes
import datetime		# Module format date & heure

##################################################################################################################
#	LES VARIABLES
#=======================================================#
now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
DirWork = "/root/Work"
FicLOG = DirWork + "/debug.log"
fichiermdp = open("/root/.pwd" , "r")
FicInventaire = DirWork + "/invent.log"
retourfonction = ""
compteur = 0

##################################################################################################################
#	LES FONCTIONS
#=======================================================#


#===================================================#
#	Fonction Génération de chaîne
#===================================================#
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
#===================================================#
#	Fonction session SSH
#===================================================#
def sessionssh(ip, TXT):
    readInvent = open(FicInventaire,"r")	# ouverture de l'inventaire en lecture seule
    lignes = readInvent.readlines()
	# afin de ne pas tenter inutilement de redéposer le certif du serveur : on verifie dans l'inventaire
    for ligne in lignes:
        #print("ligne = " + str(lignes))
        
        if ip in ligne:
            MSG = ip + " ### La clé du serveur déja présente sur le client"
            # print(MSG) 
            logging.info(MSG)
        else:
            MSG = ip + " ### Nouvelle clé du serveur à déployer"
            # print(MSG) 
            cmd= ("sshpass -f /root/.pwd ssh-copy-id -i /root/.ssh/id_rsa.pub root@" + ip)
            try:
                os.system(cmd)
                MSG = ip + " ### Dépot de la clé publique sur le client"
                logging.info(MSG)
                statut = "success"
            except:
                logging.error(ip + " ### Un pb est survenu lors du depot de la clé")
                statut = "error"
            return statut

#===================================================#
#	Fonction paramètres à déployer			
#===================================================#
def parametres(compteur):
	# initialisation du tableau qui stockera les parametres
    paramClient = []
	# ajustement du compteur à 2 caractères
    if ( compteur < 10):
        prefixecompteur = 0
    else:
        prefixecompteur = ""
	# Génération un hostname => FORLINUX_S(numéro de semaine) + compteur sur 2 car
    NumSemaine = datetime.datetime.now().strftime("%U")
    NewHostname = "FORLINUX_S" + NumSemaine + str(prefixecompteur) + str(compteur)
    paramClient.append(NewHostname) 
	# Génération  un usID stagiaire => STG_S(numéro de semaine)_compteur sur 2 car
    NewUser = "STGS" + NumSemaine + str(prefixecompteur) + str(compteur)
	
	# Génération mot passe aléatoire => appel de la fonction chaine aleatoire complexe
    nbcar = 8  
    type = "PWD"  
    password = aleatoireString(nbcar, type)
    return password, NewHostname, NewUser

#===================================================#
#	Commandes à déployer			
#===================================================#
# Changement Hostname
# On verifie que l'utilisateur ne soit pas déjà referencé dans le /etc/passwd
# suppression ancien user/home
# Création du compte utilisateur
# Changement de mot de passe


#===================================================#
#	Fonction Inventaire			
#===================================================#
def inventaire(LigneInvent):
    writeInvent = open(FicInventaire,"a")	# ouverture de l'inventaire en écriture
    writeInvent.write(LigneInvent + "\n")	# édition de l'inventaire
    writeInvent.close()		# fermeture du fichier inventaire

##################################################################################################################
#	JOURNALISATION & NIVEAU DE LOG
#=======================================================#

parser = argparse.ArgumentParser()	# Vérification de l'argument saisi lors de l'execution du script
parser.add_argument(
    "-log", 
    "--log", 
    default="warning",
    help=(
        "Préciser un niveau de journalisation."
        "Exemple --log debug', niveau par defaut ='warning'"),
    )
###
options = parser.parse_args()	# Définition du namespace exemple : --log=INFO => Namespace(log='INFO')
###
levels = {		# Création du dictionnaire des niveaux de log
    'critical': logging.CRITICAL,	# =50
    'error': logging.ERROR,			# =40
    'warn': logging.WARNING,		# =30
    'warning': logging.WARNING,		# =30
    'info': logging.INFO,			# =20
    'debug': logging.DEBUG			# =10
}
###
level = levels.get(options.log.lower())	# Définit la correspondance niveau en numerique ex : debug=10 info=20
###
if level is None:	# Condition si la syntaxe du niveau est erroné ou n'existe pas :
    raise ValueError(
        f"Niveau de log envoyé: {options.log}"
        f" -- devrait être : {' | '.join(levels.keys())}")
		
### Appel de la fonction de génération de chaîne aléatoire
nbcar = 5  
type = "REQ"  
retourfonction = aleatoireString(nbcar, type)
MSG = print("retour =" + str(retourfonction)) 

### Format de ligne de log
logging.basicConfig(filename=FicLOG, format='%(asctime)s ' + str(retourfonction) +' %(message)s', level=level)
   
##################################################################################################################
#	SCANNER IP
#=======================================================#
# Tableau qui stockera les ip connectées 
ipmachines = []

logging.info('###  LOGINIT   ### DEMARRAGE DU SCANNER IP')
# Scan du réseau plage IP [1-254]
for ping in range(1,254):
    adresse = "192.168.122." + str(ping)
    socket.setdefaulttimeout(1)
# Récupération des informations
    try:
        hostname, alias, listadresse = socket.gethostbyaddr(adresse)
# Exception aucun client connecté avec IP de la plage
    except socket.herror:
        hostname = None
        alias = None
        listadresse = adresse
# On valorise le tableau avec les IP des PC connectés
    if (hostname != None):
        ipmachines.append(adresse)
# print(ipmachines)

##################################################################################################################
#	TRAITEMENT CLIENT
#=======================================================#

for ip in ipmachines:
    logging.info( ip + ' ### Le PC est présent sur le réseau')
    compteur = compteur + 1
    client = str(now)  
    param = parametres(compteur)

    dictionnaire = "Client" + str(compteur)
    dictionnaire = {}
    dictionnaire["AdresseIP"] = ip
    dictionnaire["hostname"] = str(param[1])
    dictionnaire["userid"] = str(param[2])
    dictionnaire["password"] = str(param[0])
    for cle,valeur in dictionnaire.items():
        client = client + ";" +  valeur 
    TXT = ""
    statut = sessionssh(ip, TXT)
    if (statut != "error"):
        print(client)
        inventaire(str(client))

