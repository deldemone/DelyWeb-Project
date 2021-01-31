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
now = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
DirWork = "/root/Work"
FicLOG = DirWork + "/debug.log"
fichiermdp = open("/root/.pwd" , "r")
security = str(fichiermdp.read())
FicInventaire = DirWork + "/invent.log"
NewUser = ""
retourfonction = ""
compteur=0
resultat = ""


##################################################################################################################
#	LES FONCTIONS
#=======================================================#


#===================================================#
#	Fonction Génération de chaîne
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

# Exemple d'appel de fonction avec précision nb caractères et le type (REQ = Requête; PWD = Password; User)
# nbcar = 8  
# type = "REQ"  
# aleatoireString(nbcar, type)
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
            MSG = ip + " ### La clé du serveur déja présente sur le client"
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
            MSG = ip + " ### SUCCESS -Dépot de la clé publique sur le client "
            logging.info(MSG)
            print(MSG)
            statut = "success"
        except Exception as e:
            print(e)
            logging.error(ip + " ### Un pb est survenu lors du depot de la clé")
            statut = "error"
        return statut

def sessionssh(ip, userID, password):
### ouverture de la session ssh
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(ip, username="root", password=str(security))
        MSG = "### SUCCESS ### Connexion ssh vers " + ip
        logging.info(MSG)
        print(MSG)
        sshsuccess = True
    except Exception as e:
        print(e)
        logging.warning("### ERROR ### " + str(e))
        sshsuccess = False
### ouverture de la session sftp et copy du script de deploiement
    if (sshsuccess == True):
        try:
            sftp = ssh.open_sftp()
            logging.info("### SUCCESS ### Ouverture session sftp")
            sftp.put('/partage/deploy.py', '/tmp/deploy.py')
            logging.info("### SUCCESS ### Dépôt du script python sur le client")
            sftp.close()
            logging.info("### SUCCESS ### Fermeture session sftp")
            sftpsuccess = True
            print("### SUCCESS ### Déploiement du script sur le client")
        except Exception as e:
            print(e)
            logging.warning("### ERROR ### " + str(e))
            sftpsuccess = False
### exécution du script de déploiement
        if (sftpsuccess == True):
            try:
                stdin, stdout, stderr = ssh.exec_command('python /tmp/deploy.py --userID ' + userID + ' --pwd ' + password)
                for line in stdout.read().splitlines():
                    #print(line)
                    sortieDist = (line.decode("utf-8", "ignore"))
                    print(sortieDist)
                    logging.info(sortieDist)
                logging.info("### SUCCESS ### Exécution du script de déploiement")
                ssh.close()
                logging.info("### SUCCESS ### Fermeture de la session ssh")
            except Exception as e:
                print(e)
                logging.warning("### ERROR ### " + str(e))
                success = False	
    
        
#===================================================#
#	Fonction paramètres à déployer			
#===================================================#
def parametres (ip):
	# initialisation du tableau qui stockera les parametres
# Récuperation de l'adresse mac
    mac = ""
    writemac = os.system("arp -a " + ip + " | awk -F\" \" '{print $4}'> tmp")
    mon_fichiermac=open("tmp","r")
    mactmp = str(mon_fichiermac.read())
    mac = mac.rstrip("\n")
# Récuperation du hostname
    host = ""
    writehost = os.system("arp -a " + ip + " | awk -F\" \" '{print $1}'> tmp")
    mon_fichierhost=open("tmp","r")
    host = str(mon_fichierhost.read())
# Génération  un usID stagiaire => STG_S(numéro de semaine)_compteur sur 2 car
    nbcar = 4  
    type = "USER"  
    IDuser = aleatoireString(nbcar, type)
    NumSemaine = datetime.datetime.now().strftime("%U")
    NewUser = "STGS" + NumSemaine + "-" + str(IDuser)
	
# Génération mot passe aléatoire => appel de la fonction chaine aleatoire complexe
    nbcar = 8  
    type = "PWD"  
    password = aleatoireString(nbcar, type)
    logging.info("### SUCCESS ### Génération des paramétres")
    return password, NewUser, mac
	
#===================================================#
#	INITIALISATION DE FICHIER SI NON EXISTANT
#===================================================#
def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        fichier= open(filePath, 'w')
        fichier.close()


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
    try:
        writeInvent = open(FicInventaire,"a")	# ouverture de l'inventaire en écriture
        writeInvent.write(LigneInvent + "\n")	# édition de l'inventaire
        writeInvent.close()		# fermeture du fichier inventaire
        logging.info("Inscription dans l'inventaire " + FicInventaire)
    except:
        logging.info("Aucune inscription dans l'inventaire " + FicInventaire)


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

##################################################################################################################
#	xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
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

##################################################################################################################
#	SCANNER IP
#=======================================================#
reseau = args.reseau

# Tableau qui stockera les ip connectées 
ipmachines = []
logging.info("################################################################")
logging.info('### LOGINIT ### DEMARRAGE DU SCANNER IP')

# Scan du réseau plage IP [1-254]
for ping in range(2,254):
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
# vérifcation que les fichiers requis sont existants, dans la négative Création de ces fichiers
checkFileExistance(FicInventaire)
for ip in ipmachines:
    
    logging.info( ip + ' ### Le PC est présent sur le réseau')
    param = parametres(ip)

    TXT = ""
    password = str(param[0])
    mac = str(param[2])
    userID = str(param[1])
    statut = sshpass(ip, TXT, mac)
    client = str(now) + ";" + mac + ";" + ip + ";" + userID + ";" + password
    logging.info("################################################################")
    if (statut != "error"):
        sessionssh(ip, userID, password)
        logging.info("################################################################")
        inventaire(str(client))
        #time.sleep(5)
        logging.info("################################################################")

