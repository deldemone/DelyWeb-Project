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
import sys
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
    present = False
    for ligne in lignes:
        #print("ligne = " + str(lignes))   
        if ip in ligne:
            MSG = ip + " ### La clé du serveur déja présente sur le client"
            print(MSG)
            present = True
            statut = ""
            break
            #logging.info(MSG)
    if (present == False):
        MSG = ip + " ### Nouvelle clé du serveur à déployer"
        print(MSG) 
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
if len(sys.argv) != 3:
    print("usage : encours.py --log=debug|info|warn --reseau=192.168.1.0")
    sys.exit(1)

### Récuperation du niveau de log
separateur = "="
niveaulog = sys.argv[1]
niveau = separateur.join(niveaulog.split(separateur)[1:])
nivLog = getattr(logging, niveau.upper(), None)
print(nivLog)
if ( nivLog == None ):
    raise ValueError('Niveau de log invalide, vous avez saisi : %s' % niveau + '\n usage : encours.py --log=debug|info|warn --reseau=192.168.1.0')

### Géneration d'un numéro de requête : Appel de la fonction aleatoireString
nbcar = 5  
type = "REQ"  
retourfonction = aleatoireString(nbcar, type)
MSG = print("retour =" + str(retourfonction)) 

### Format de ligne de log
logging.basicConfig(filename=FicLOG, format='%(asctime)s ' + str(retourfonction) +' %(message)s', level=nivLog)

   
##################################################################################################################
#	SCANNER IP
#=======================================================#
separateur = "="
argument2 = sys.argv[2]
reseau = separateur.join(argument2.split(separateur)[1:])
#print("reseau : " + reseau)
# Tableau qui stockera les ip connectées 
ipmachines = []
logging.info('###  LOGINIT   ### DEMARRAGE DU SCANNER IP')

# Scan du réseau plage IP [1-254]
for ping in range(1,254):
    if ( str(reseau) != ""):
        separateur = "."
        network = separateur.join(reseau.split(separateur)[:-1]) + "."
        #print("network:" + str(network))
        adresse = network + str(ping)
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
    else:
        exit("Merci de renseigner le sous-réseau à reinitialiser : exemple Python3 encours.py --log=debug 192.168.1.0")
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
        #print(client)
        inventaire(str(client))

