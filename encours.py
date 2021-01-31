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
from string import punctuation, ascii_letters, digits, ascii_uppercase	# module des opérations usuelles sur les chaînes
import datetime		# Module format date & heure
import time
import paramiko


##################################################################################################################
#	LES VARIABLES
#=======================================================#
### REPERTOIRES
DirWork = "/root/Work"
LOG = DirWork + "/log"
DirStagiaire = DirWork + "/FicSTGS"
dicoREP = {}
dicoREP["DirWork"] = DirWork
dicoREP["DirStagiaire"] = DirStagiaire
dicoREP["LOG"] = LOG

### FICHIERS OUTPUT
FicLOG = DirWork + "/debug.log"
FicInventaire = DirWork + "/invent.log"

### FICHIERS INPUT
fichiermdp = "/root/.pwd"
openFicMDP = open("/root/.pwd" , "r")
security = str(openFicMDP.read())

FicInventaire = DirWork + "/invent.log"
dicoFIC =  {}
dicoFIC["mdp"] = fichiermdp
dicoFIC["inventaire"] = FicInventaire

### VARIABLES GLOBALES
NewUser = ""
retourfonction = ""
resultat = ""

# CADRE & PREFIXE LOG
PLEIN = "################################################################"
LIGHT = "================================================================"
INTER = "###############"
OK = " ##  OK  ## *** LOC  - "
KO = " ##  KO  ## *** LOC  - "
SO = " ##  SO  ## *** LOC  - "
INFO = " ## INFO ## *** LOC  - "
STEP = " ## STEP ## *** LOC  - "
now = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")

##############################################################################################
#################### 		LES FONCTIONS

#===================================================#
#	INITIALISATION DES REPERTOIRES SI NON EXISTANT
#===================================================#
def checkRepertoireExistance(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            MSG = OK +  "Création " + path
            logging.info(MSG)
        except CreatePathError as e:
            logging.error(KO + e)
    else:
        MSG = OK + path + " existant"
        logging.info(MSG)

#===================================================#
#	INITIALISATION DES FICHIERS SI NON EXISTANT
#===================================================#
def checkFileExistance(fic):
    if not os.path.isfile(fic):
        try:
            fichier= open(fic, 'w')
            logging.info(OK + "Création " + fic)
            fichier.close()
        except CreateFileError as e:
            logging.error(KO + e)
    else:
        MSG = OK + fic + " existant"
        logging.info(MSG)    

#===================================================#
#	FONCTION DE GENERATION DE CHAINE ALEATOIRE
#===================================================#
def aleatoireString(nbcar, type):
    # On détermine la complexité de la chaine à génèrer...
    alphanum = ascii_uppercase + digits
    symbols = ascii_letters + digits # + punctuation
    #...en fonction du type de chaine souhaité
    if (type == "REQ"):
            complexe = alphanum
            prefixe = type
    elif (type == "PWD"):
            complexe = symbols
            prefixe = ""
    elif (type == "USER"):
            complexe = digits
            prefixe = ""
    # Génération de la chaine aléatoire avec le module random
    Str_aleatoire = random.SystemRandom()
    resultat = ""
    resultat = "".join(Str_aleatoire.choice(complexe) for i in range(nbcar))
    chaine_alea = prefixe + resultat
    return chaine_alea

#===================================================#
#	Fonction SSHPASS
#===================================================#
def sshpass(ip, TXT, mac):
    readInvent = open(FicInventaire,"r")	# ouverture de l'inventaire en lecture seule
    lignes = readInvent.readlines()
	# afin de ne pas tenter inutilement de redéposer le certif du serveur : on verifie dans l'inventaire
    present = False
    for ligne in lignes:
        #print("ligne = " + str(lignes))   
        if mac in ligne:
            MSG = OK + "La clé du serveur déja présente sur client"
            logging.info(MSG)
            present = True
            statut = "ok"
            break
            #logging.info(MSG)
    if (present == False):
        MSG = ip + " ### Nouvelle clé du serveur à déployer"
        logging.info(MSG)
        cmd= ("sshpass -f /root/.pwd ssh-copy-id -i /root/.ssh/id_rsa.pub root@" + ip +"; exit")
        try:
            #ssh = paramiko.SSHClient() 
            os.system(cmd)
            MSG = OK + "Dépot de la clé publique sur le client "
            logging.info(MSG)
            print(MSG)
            statut = "success"
        except Exception as e:
            print(e)
            logging.error(KO + "Un pb est survenu lors du depot de la clé")
            statut = "error"
        return statut

def sessionssh(ip, userID, password):
### ouverture de la session ssh
    try:
        MSG = STEP + "Initialisation de la connexion ssh"
        logging.info(MSG)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(ip, username="root", password=str(security))
        MSG = OK + "Connexion ssh vers " + ip
        logging.info(MSG)
        print(MSG)
        sshsuccess = True
    except Exception as e:
        print(e)
        logging.warning(KO + str(e))
        sshsuccess = False
### ouverture de la session sftp et copy du script de deploiement
    if (sshsuccess == True):
        try:
            logging.info(LIGHT)
            MSG = STEP + "Dépôt du script via le SFTP"
            logging.info(MSG)
            sftp = ssh.open_sftp()
            logging.info(OK + "Ouverture session sftp")
            sftp.put('/partage/deploy.py', '/tmp/deploy.py')
            logging.info(OK + "Dépôt du script python sur le client")
            sftp.close()
            logging.info(OK + "Fermeture session sftp")
            sftpsuccess = True
            print(OK + "Déploiement du script sur le client")
        except Exception as e:
            print(e)
            logging.warning(KO + str(e))
            sftpsuccess = False
### exécution du script de déploiement
        if (sftpsuccess == True):
            try:
                logging.info(LIGHT)
                stdin, stdout, stderr = ssh.exec_command('python /tmp/deploy.py --userID ' + userID + ' --pwd ' + password)
                for line in stdout.read().splitlines():
                    sortieDist = (line.decode("utf-8", "ignore"))
                    print(sortieDist)
                    if sortieDist != "":
                        logging.info(sortieDist)
                logging.info(OK + "Exécution du script de déploiement terminée")
            except Exception as e:
                print(e)
                logging.error( KO + str(e))
                success = False	
    try:
        ssh.close()
        logging.info(OK + "Fermeture de la session ssh")   
    except Exception as e:
        print(e)
        logging.error( KO + str(e))
        
#===================================================#
#	Fonction paramètres à déployer			
#===================================================#
def parametres (ip):
	# initialisation du tableau qui stockera les parametres
    countError = 0
# Récuperation de l'adresse mac
    mac = ""
    try:
        writemac = os.system("arp -a " + ip + " | awk -F\" \" '{print $4}'> tmp")
        mon_fichiermac=open("tmp","r")
        mactmp = str(mon_fichiermac.read())
        mac = mac.rstrip("\n")   
    except:
        logging.error(KO + "Récupération MAC")
        countError = countError + 1
# Récuperation du hostname
    host = ""
    try:
        writehost = os.system("arp -a " + ip + " | awk -F\" \" '{print $1}'> tmp")
        mon_fichierhost=open("tmp","r")
        host = str(mon_fichierhost.read())
    except:
        logging.error(KO + "Récupération MAC")
        countError = countError + 1
# Génération  un usID stagiaire => STG_S(numéro de semaine)_compteur sur 2 car
    nbcar = 4  
    type = "USER"
    try:
        IDuser = aleatoireString(nbcar, type)
        NumSemaine = datetime.datetime.now().strftime("%U")
        NewUser = "STGS" + NumSemaine + "-" + str(IDuser)
    except:
        countError = countError + 1
# Génération mot passe aléatoire => appel de la fonction chaine aleatoire complexe
    nbcar = 8  
    type = "PWD"  
    try:
        password = aleatoireString(nbcar, type)
    except:
        countError = countError + 1
# Gestion compteur erreurs
    if countError == 0:
        logging.info(OK + "Génération des paramétres")
        return password, NewUser, mac
    else:
        MSG = KO + "lors de la génération des paramétres"
        logging.info(MSG)
        print(MSG)

#===================================================#
#	Fonction Inventaire			
#===================================================#
def inventaire(LigneInvent):
    try:
        logging.info(STEP + "Inscription dans l'inventaire" + FicInventaire)
        writeInvent = open(FicInventaire,"a")	# ouverture de l'inventaire en écriture
        writeInvent.write(LigneInvent + "\n")	# édition de l'inventaire
        writeInvent.close()		# fermeture du fichier inventaire
        logging.info(OK + "Nouvelle entrée dans l'inventaire")
    except:
        logging.info(KO + "Aucune inscription dans l'inventaire ")


##################################################################################################################
#	Définition des arguments
#=======================================================#

parser = argparse.ArgumentParser('Executer ce script requiert deux arguments --log et --reseau ')

parser.add_argument('--reseau',
                    type=str,
                    help='Préciser le reseau cible ex: --reseau=192.168.122.0',
                    required=True)
parser.add_argument('--log',
                    type=str,
                    help='Usage : --log=debug|info|warn',
                    required=True)
args = parser.parse_args()

#=======================================================#
### Récuperation du niveau de log
niveau = args.log
nivLog = getattr(logging, niveau.upper(), None)

if ( nivLog == None ):
    raise ValueError('Niveau de log invalide, vous avez saisi : %s' % niveau + '\n usage : encours.py --log=debug|info|warn --reseau=192.168.1.0')

### Géneration d'un numéro de requête : Appel de la fonction aleatoireString
nbcar = 5  
type = "REQ"  
retourfonction = aleatoireString(nbcar, type)

### Format de ligne de log
logging.basicConfig(filename=FicLOG, filemode='w', format='%(asctime)s ' + str(retourfonction) +' %(message)s', level=nivLog)


############# INITIALISATION DU LOG #################

logging.info(PLEIN)
logging.info(INTER + "     DEBUT EXECUTION DU SCRIPT    " + INTER)
logging.info(PLEIN)

##################################################################################################################
#	INITIALISATION DE L'ENVIRONNEMENT DE TRAVAIL
#=======================================================#
# Vérification arborescence serveur
MSG = STEP +  "Contrôle arborescence"
logging.info(MSG)
for cle,path in dicoREP.items():
    checkRepertoireExistance(path)
logging.info(LIGHT)
# vérifcation que les fichiers requis sont existants, dans la négative Création de ces fichiers
MSG = STEP +  "Contrôle des fichiers requis"
logging.info(MSG)
for cle,fic in dicoFIC.items():
    checkFileExistance(fic)

##################################################################################################################
#	SCANNER IP
#=======================================================#
reseau = args.reseau
logging.info(LIGHT)
os.system('clear')
print(PLEIN)
MSG = STEP + 'Démarrage du scanner IP'
logging.info(MSG)
print(MSG)
print(LIGHT)

# Tableau qui stockera les ip connectées 
ipmachines = []
# Scan du réseau plage IP [1-254]
for ping in range(2,254):
    if ( str(reseau) != ""):
        separateur = "."
        network = separateur.join(reseau.split(separateur)[:-1]) + "."
        adresse = network + str(ping)
        socket.setdefaulttimeout(1)
# Récupération des informations
        try:
            hostname, alias, listadresse = socket.gethostbyaddr(adresse)
            MSG = INFO + adresse + ' est actif sur le réseau'
            logging.info(MSG)
            print(MSG)
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

##################################################################################################################
#	TRAITEMENT CLIENT
#=======================================================#

for ip in ipmachines:
    logging.info(PLEIN)
    print("")
    MSG = STEP + "TRAITEMENT DE " + ip
    print(MSG)
    print(LIGHT)
    logging.info(MSG)
    logging.info(PLEIN)
    logging.info(STEP + "Déclenchement génération paramètres distants")
    param = parametres(ip)

    TXT = ""
    password = str(param[0])
    mac = str(param[2])
    userID = str(param[1])
    logging.info(LIGHT)
    logging.info(STEP + "Verification prérequis sécurité SSH")
    statut = sshpass(ip, TXT, mac)

    client = str(now) + ";" + mac + ";" + ip + ";" + userID + ";" + password
    logging.info(LIGHT)
    if (statut != "error"):
        sessionssh(ip, userID, password)
        logging.info(LIGHT)
        inventaire(str(client))
        #time.sleep(5)
        logging.info(LIGHT)
logging.info(PLEIN)
print(PLEIN)
MSG = STEP + 'TRAITEMENT TERMINE'
logging.info(MSG)
print(MSG)
print(PLEIN)
print("")
logging.info(PLEIN)
