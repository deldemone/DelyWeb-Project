#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Nom :			 RenewDomain.py

Exécution :		RenewDomain.py --debug info|warn|debug --reseau 192.168.122.0

Action :		Permet de scanner le reseau d'un domaine 
				De parametrer les comptes utilisateurs à distance 
				De maintenir un inventaire du domaine
				De créer des fiches utilisateurs (Login, mot de passe, hostname)
				De créer des QRcode à partir de l'adresse mac à apposer sur les postes de travail
"""


##################################################################################################################
__author__ = "Delphine Durand Demongeot"
__version__ = "1.0.0"
__email__ = "dd0275416@gmail.com"
__status__ = "En cours de rédaction"

########################################################################
####################		LES MODULES			
########################################################################

import sys			# module accès aux paramètres et fonctions propres aux systèmes
import socket		# module communication réseau
import os			# module pour le système d'exploitation
import logging		# module de journalisation
import argparse 	# module d'analyse de ligne de commande
import random		# module génèration des nombres pseudo-aléatoires
from string import punctuation, ascii_letters, digits, ascii_uppercase	# module des opérations usuelles sur les chaînes
import datetime		# module format date & heure
import paramiko		# module permettant de programmer l’envoi de commandes à un équipement réseau via le protocole SSH
import qrcode		# module permettant de gérer des QRCode
from PIL import ImageDraw, Image, ImageFont	# module permettant la manipulation des images QRcode 
import glob			# module utilisé pour traitement sur les extensions

########################################################################
####################		LES VARIABLES			
########################################################################

### VARIABLES GLOBALES

RetourFonctionAleatoireString = ""
now = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
NumSemaine = datetime.datetime.now().strftime("%U")

### LES REPERTOIRES
DossierWork = "/root/Work"
LOG = "/var/log"
RepertoireFicheUtilisateur = DossierWork + "/UserSemaine" + NumSemaine
RepertoireFichePC = DossierWork + "/FichePC"
RepertoireInventaire = DossierWork + "/Inventaire"
""" Création du dictionnaire des répertoires qui permettra de créer les répertoires inexistants Fonction : checkRepertoireExistance """
dicoRepertoires = {}
dicoRepertoires["Environnement de travail"] = DossierWork
dicoRepertoires["Repertoire Fiche Utilisateur"] = RepertoireFicheUtilisateur
dicoRepertoires["Répertoire des Logs"] = LOG
dicoRepertoires["Répertoire Fiche PC"] = RepertoireFichePC
dicoRepertoires["Répertoire des Inventaires"] = RepertoireInventaire

### LES FICHIERS INPUT
fichiermdp = "/root/.pwd"
openFichierMDP = open("/root/.pwd" , "r")
security = str(openFichierMDP.read())

### FICHIERS OUTPUT
FichierLOG = LOG + "/RenewDomain.log"
InventaireUtilisateur = RepertoireInventaire + "/InventaireUtilisateurS" + NumSemaine
InventaireDomaine = RepertoireInventaire + "/InventaireDomaine"
""" Création du dictionnaire des fichiers qui permettra de créer les fichiers inexistants ainsi ques leurs entêtes Fonction : checkFileExistance """
dicoFichier =  {}
dicoFichier[FichierLOG] = ""
dicoFichier[InventaireUtilisateur] = "Horodatage création;Hostname;UserID;password"
dicoFichier[InventaireDomaine] = "Horodatage import;Hostname;Mac;Information Système"



# CADRE & PREFIXE LOG
REQ = ""
PLEIN = "################################################################"
LIGHT = "================================================================"
DEMI = "#########################################"
INTER = "###############"
OK = REQ + " ##  OK  ## *** LOC  - "
KO = REQ + " ##  KO  ## *** LOC  - "
SO = REQ + " ##  SO  ## *** LOC  - "
INFO = REQ + " ## INFO ## *** LOC  - "
STEP = REQ + " ## STEP ## *** LOC  - "

########################################################################
####################		LES FONCTIONS			
########################################################################

""""""""""""""""""""""""""""""""""""""""""""""""
""" ENVIRONNEMENT DE TRAVAIL"""
""""""""""""""""""""""""""""""""""""""""""""""""
#===================================================#
#	INITIALISATION DES REPERTOIRES SI NON EXISTANT
#===================================================#
""" Vérification de l'existance des répertoires utiles et création si non existant """
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
""" Vérification de l'existance des répertoires utiles et création si non existant """
def checkFileExistance(cle, fic):
    if not os.path.isfile(fic):
        try:
            fichier= open(fic, 'w')
            fichier.write(cle + "\n")	
            logging.info(OK + "Création " + fic)
            fichier.close()
        except Exception as e:
            logging.error(REQ + KO + str(e))
    else:
        MSG = OK + fic + " existant"
        logging.info(MSG)    

#===================================================#
#	RéINITIALISATION DU REPERTOIRE FICHES UTILISATEUR
#===================================================#
""" Suppression des anciennes fiches utilisateur """
def cleanfiche(repertoire):
    try:
        files = os.listdir(repertoire)
        logging.info(OK + "Suppression anciennes fiches utilisateur")
        for filename in os.listdir(repertoire) :
            os.remove(repertoire + "/" + filename)
            
    except:
        logging.error(Ko + "PB de Réinit. répertoire fiche utilisateur")

""""""""""""""""""""""""""""""""""""""""""""""""
""" FONCTION OUTIL & PARAMETRES"""
""""""""""""""""""""""""""""""""""""""""""""""""

#===================================================#
#	FONCTION DE GENERATION DE CHAINE ALEATOIRE
#===================================================#
def aleatoireString(nbcar, type):
    # On détermine la complexité de la chaine à génèrer...
    alphanum = ascii_uppercase + digits
    symbols = ascii_letters + digits # + punctuation
    #...en fonction du type de chaine souhaité
    if (type == "REQ"):
            complexe = digits #alphanum
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
#	FONCTION NETTOYAGE	
#===================================================#
def cleanWork(extension, REQ):
    """ Suppression des fichiers suivants leur extension"""
    try:
        for fichier in glob.glob(extension):
            os.remove(fichier)
    except Exception as e:
        logging.error(REQ + KO + str(e))   
		
#===================================================#
#	FONCTION GENERATION/RECUPERATION DE PARAMETRES	
#===================================================#
def parametres (ip, REQ):
	# initialisation du tableau qui stockera les parametres
    countError = 0
# Récuperation de l'adresse mac
    mac = ""
    try:
        writemac = os.system("arp -a " + ip + " | awk -F\" \" '{print $4}'> mac.tmp")
        mon_fichiermac=open("mac.tmp","r")
        mactmp = str(mon_fichiermac.read())
        mac = mactmp.rstrip("\n")   
    except:
        logging.error(REQ + KO + "Récupération MAC")
        countError = countError + 1
# Récuperation du hostname
    host = ""
    try:
        writehost = os.system("arp -a " + ip + " | awk -F\" \" '{print $1}'> host.tmp")
        mon_fichierhost=open("host.tmp","r")
        hosttmp = str(mon_fichierhost.read())
        host = hosttmp.rstrip("\n")
    except:
        logging.error(REQ + KO + "Récupération MAC")
        countError = countError + 1
# Génération  un usID utilisateur => STG_S(numéro de semaine)_compteur sur 2 car
    nbcar = 4  
    type = "USER"
    NewUser = ""
    try:
        IDuser = aleatoireString(nbcar, type)
        NewUser = "USERS0" + NumSemaine + "-" + str(IDuser)
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
        logging.info(REQ + OK + "Génération des paramétres")
        return password, NewUser, mac, host
    else:
        PRINT = KO + "lors de la génération des paramétres"
        print(PRINT)
        MSG = REQ + PRINT
        logging.info(MSG)


""""""""""""""""""""""""""""""""""""""""""""""""
""" FONCTION DE CONNEXION DISTANTE """
""""""""""""""""""""""""""""""""""""""""""""""""
#===================================================#
#	FONCTION SSHPASS
#===================================================#
def sshpass(ip, TXT, mac, REQ):
    """ La fonction verifie que l'adresse mac ne soit pas déjà référencé dans l'inventaire
        si cet échange n'a pas déjà été effectué, 
        => déploiement de la clé publique du serveur sur le client distant 
        si le statut retourné est error le traitement de ce client sera annulé.
    """
    readInvent = open(InventaireDomaine,"r")	# ouverture de l'inventaire en lecture seule
    lignes = readInvent.readlines()
	# afin de ne pas tenter inutilement de redéposer le certif du serveur : on verifie dans l'inventaire
    present = False
    for ligne in lignes:  
        if mac in ligne:
            logging.info(REQ + OK + "La clé du serveur déja présente sur client")
            present = True
            statut = "MacPresentInventaire"
            break
    if (present == False):
        logging.info(REQ + INFO + "Nouvelle clé du serveur à déployer")
        cmd= ("sshpass -f /root/.pwd ssh-copy-id -i /root/.ssh/id_rsa.pub root@" + ip +"; exit")
        try:
            #ssh = paramiko.SSHClient() 
            os.system(cmd)
            # Sortie console
            PRINT = OK + "Dépot de la clé publique sur le client "
            print(PRINT)
            # Sortie log
            MSG = REQ + PRINT
            logging.info(MSG)
            statut = "success"
        except Exception as e:
            print(e)
            logging.error(REQ + KO + "Un pb est survenu lors du depot de la clé")
            statut = "error"
        return statut
#===================================================#
#	FONCTION SESSION SSH
#===================================================#
def sessionssh(ip, userID, password, REQ):
    """ la session ssh se déroule en 3 étapes séquentielles qui dépendent de la bonne éxecution de la précédente
        la connexion ssh entre le serveur et le PC distant
        la connexion sftp avec depôt du script deploy.py sur le PC distant
        execution du script distant
    """
### ouverture de la session ssh
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(ip, username="root", password=str(security))
        sshsuccess = True
        # Sortie console
        PRINT = OK + "Connexion ssh vers " + ip
        print(PRINT)
        # Sortie log
        logging.info(REQ + PRINT)
    except Exception as e:
        print(e)
        logging.error(REQ + KO + str(e))
        sshsuccess = False
    ### ouverture de la session sftp et copy du script de deploiement
    if (sshsuccess == True):
        try:
            logging.info(LIGHT)
            logging.info(REQ + STEP + "Dépôt du script via le SFTP")
            sftp = ssh.open_sftp()
            sftp.put('/partage/deploy.py', '/tmp/deploy.py')
            logging.info(REQ + OK + "Dépôt du script python sur le client")
            sftp.close()
            sftpsuccess = True
            print(OK + "Déploiement du script sur le client")
        except Exception as e:
            print(e)
            logging.error(KO + str(e))
            sftpsuccess = False
        ### exécution du script de déploiement
        if (sftpsuccess == True):
            try:
                logging.info(LIGHT)
                stdin, stdout, stderr = ssh.exec_command('python /tmp/deploy.py --userID ' + userID + ' --pwd ' + password)
                for line in stdout.read().splitlines():
                    sortieDist = (line.decode("utf-8", "ignore"))
                    if sortieDist != "" and "System" not in sortieDist:
                        print(sortieDist)
                        logging.info(REQ + sortieDist)
                    if "System" in sortieDist:
                        system = sortieDist
                logging.info(REQ + OK + "Exécution du script de déploiement terminée")
            except Exception as e:
                print(e)
                logging.error( KO + str(e))
                success = False	
    try:
        ssh.close()
        logging.info(REQ + OK + "Fermeture de la session ssh")   
    except Exception as e:
        print(e)
        logging.error(REQ + KO + str(e))
    logging.info(LIGHT)
    return system    

""""""""""""""""""""""""""""""""""""""""""""""""
""" GENERATION DES FICHIERS DE SORTIE """
""""""""""""""""""""""""""""""""""""""""""""""""
#===================================================#
#	FONCTION DES INVENTAIRES 
#===================================================#
def Inventaire(LigneInvent, typeInvent, mac, REQ):
    try:
        OpenInventaire = open(typeInvent,"r")	# ouverture de l'inventaire en lecture
        lignesInvent = OpenInventaire.readlines()
        Present = False
        for ligne in lignesInvent:		
            if mac in ligne:
                Present = True
        if Present == False:
            logging.info(REQ + STEP + "Inscription dans l'inventaire" + typeInvent)
            writeInvent = open(typeInvent,"a")	# ouverture de l'inventaire en écriture
            writeInvent.write(LigneInvent + "\n")	# édition de l'inventaire
            writeInvent.close()		# fermeture du fichier inventaire
            logging.info(REQ + OK + "Nouvelle entrée dans l'inventaire" + typeInvent)
        else:
            logging.info(REQ + OK + "Entrée déjà présente dans inventaire" + typeInvent)
    except:
        logging.info(REQ + KO + "Aucune inscription dans l'inventaire " + typeInvent)

#===================================================#
#	CREATION FICHE UTILISATEUR			
#===================================================#

def CreationFicheUtilisateur(userID, password, host, REQ):
    """ Création de la fiche à communiquer à l'utilisateur 
        qui précise les indication suivante
        Hostname, Login utilisateur, Mdp utilisateur
    """
    try:
        fiche = RepertoireFicheUtilisateur + "/" + userID
        fichier = open(fiche, 'w')
        try:
            fichier.write("\n" + PLEIN + "\n \n")
            fichier.write("		Formation Linux Semaine " + NumSemaine + "\n \n")
            fichier.write(LIGHT + "\n \n")
            fichier.write("	Hostname	=	" + host + "\n")
            fichier.write("	Login utilisateur	=	" + userID + "\n")
            fichier.write("	Mot de passe	=	" + password + "\n \n")
            fichier.write("\n" + PLEIN + "\n \n")
            fichier.close()
            logging.info(REQ + OK + "Création de la fiche" + userID)
            return fiche
        except:
            logging.info(REQ + KO + "Lors de l'édition de la fiche utilisateur")
    except:
        logging.info(REQ + KO + "Lors de la création de la fiche utilisateur")
#===================================================#
#	CREATION FICHE PC = QRCODE			
#===================================================#    
def QRcodePC(mac, host, REQ):
    """ Création de la fiche PC 
        génération d'un QRcode à partir de l'adresse mac
        on ajoute également le hostname au dessus de ce qrcode
    """
    NameJPGMac = mac.replace(':', '') + ".jpg"
    FilePath = RepertoireFichePC + "/" + NameJPGMac
    if not os.path.isfile(FilePath):
        try:
            image = qrcode.make(mac)
            typefont = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
            fnt=ImageFont.truetype(typefont, 40)
            draw = ImageDraw.Draw(image)
            qr_x, qr_y = image.size
            draw.text((qr_x/4,0), 
            text=host,
            font=fnt,
            fill=0)
            image.save(FilePath) 
            logging.info(REQ + OK + "Création de la fiche " + NameJPGMac)
            return FilePath
        except Exception as e:
            logging.error(REQ + KO + str(e))
    else:
        logging.info(REQ + OK + NameJPGMac + " existant sous " + RepertoireFichePC) 
        FilePath=""
        return FilePath
	

########################################################################
####################		EXECUTION DU SCRIPT		
########################################################################
""" L'execution du script néccessite deux parémètres obligatoires
--log debug|info|warn
--reseau le réseau cible 
et un facultatif --range ipdebut,ipfin								"""
#===================================================#
#	LES PARAMETRES			
#===================================================#  
parser = argparse.ArgumentParser('Executer ce script requiert deux arguments obligatoire --log et --reseau et un facultatif --range')

parser.add_argument('--log',
                    type=str,
                    help='Usage : --log=debug|info|warn',
                    required=True)
parser.add_argument('--reseau',
                    type=str,
                    help='Préciser les 3 premiers octetde votre reseau cible ex: --reseau=192.168.122',
                    required=True)
parser.add_argument('--range',
                    type=str,
                    help='Préciser l\'étendue cible ex: --range=4,64 /n Par défaut la range 1,254 sera appliquée',
                    required=False)
args = parser.parse_args()

#===================================================#
#	LE NIVEAU DE LOG			
#===================================================#  
""" on récupère le niveau de log
DEBUG	:	Information détaillée, intéressante seulement lorsqu'on diagnostique un problème
INFO	:	Confirmation que tout fonctionne comme prévu.
WARNING	:	L'indication que quelque chose d'inattendu a eu lieu, ou de la possibilité d'un problème dans un futur proche 
(par exemple « espace disque faible »). Le script fonctionne encore normalement.
ERROR	:	Du fait d'un problème plus sérieux, le logiciel n'a pas été capable de réaliser une tâche.
CRITICAL:	Une erreur sérieuse, indiquant que le programme lui-même pourrait être incapable de continuer à fonctionner.
"""
#Récuperation du niveau de log
niveau = args.log 
nivLog = getattr(logging, niveau.upper(), None)

""" puis on détermine en parcourant le module logging sa valeur numerique
Niveau		==> Valeur Numérique
CRITICAL	==>50
ERROR		==>40
WARNING		==>30
INFO		==>20
DEBUG		==>10
"""

if ( nivLog == None ):
    raise ValueError('Niveau de log invalide, vous avez saisi : %s' % niveau + '\n usage : encours.py --log=debug|info|warn --reseau=192.168.1.0')


#Formatage de ligne de log
logging.basicConfig(filename=FichierLOG, filemode='w', format='%(asctime)s ' + ' %(message)s', level=nivLog)

#####################################################
####	INITIALISATION DU LOG				
#####################################################

logging.info(PLEIN)
logging.info(INTER + "     DEBUT EXECUTION DU SCRIPT    " + INTER)
logging.info(PLEIN)

#####################################################
####	PREPARATION DE L'ENVIRONNEMENT DE TRAVAIL
#####################################################


# Vérification arborescence serveur
logging.info(STEP +  "Contrôle arborescence")
logging.info(LIGHT)
for cle,path in dicoRepertoires.items():
    checkRepertoireExistance(path)


# vérifcation que les fichiers requis sont existants, dans la négative Création de ces fichiers
logging.info(PLEIN)
logging.info(STEP +  "Contrôle des fichiers requis")
logging.info(LIGHT)
for cle,fic in dicoFichier.items():
    checkFileExistance(fic, cle)
	
# création du lien symbolique du log
os.system("ln -s " + FichierLOG + " " + DossierWork)

# Suppression des anciennes fiches Utilisateurs
repertoire = RepertoireFicheUtilisateur
cleanfiche(repertoire)

#####################################################
####	SCANNER IP
#####################################################
""" Le scanner ip fonctionne de la manière suivante :
    Il récupère le paramètre --réseau qui correspond au 3 premiers octets de la cible
    Si une range est définit il scannera uniquement l'étendue précisée 
    exemple : Python3 RenewDomain.py --reseau 192.168.122 --range 3,10
    Le range par défaut est 1,254 """
# Sortie console
os.system('clear')
print(PLEIN)
MSG = STEP + 'Démarrage du scanner IP'
print(MSG)
print(LIGHT)

# Sortie log
logging.info(PLEIN)
logging.info(MSG)

### On récupère les paramètres
# le --reseau 
reseau = args.reseau

# L'étendue cible si elle a été précisée
etenduecible = args.range

if args.range != "" :
    separateur = ","
    IPdebut = separateur.join(etenduecible.split(separateur)[:-1])
    IPfin = separateur.join(etenduecible.split(separateur)[1:])
else:
    IPdebut = 2
    IPfin = 254
    print (IPdebut + "<>" + IPfin)

# Tableau qui stockera les ip connectées 
ipmachines = []
# Scan du réseau plage IP [1-254]
for ping in range(int(IPdebut),int(IPfin)):
    if ( str(reseau) != ""):
        adresse = reseau + "." + str(ping)
        socket.setdefaulttimeout(1)
# Récupération des adresses ip
        try:
            hostname, alias, listadresse = socket.gethostbyaddr(adresse)
            # Sortie console
            PRINT = INFO + adresse + ' est actif sur le réseau'
            print(PRINT)
            # Sortie log
            MSG = REQ + PRINT
            logging.info(MSG)

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
if ipmachines == [] :
    # Sortie console
    PRINT = KO + "Aucun client sur la range : " + IPdebut + " <> " + IPfin
    print (PRINT)
    # Sortie log
    MSG = REQ + PRINT
    logging.info(MSG)

##################################################################################################################
#	TRAITEMENT CLIENT
#=======================================================#


for ip in ipmachines:

    #Géneration du numéro de requête sur 5 caractères avec prefixe REQ: Appel de la fonction aleatoireString
    """ A chaque traitement de client nous générons un numero de reqête unique"""
    nbcar = 5  
    type = "REQ"  
    REQ = aleatoireString(nbcar, type)

    # Initialisation du traitement
    # Sortie console
    print("")
    PRINT = STEP + "TRAITEMENT DE " + ip
    print(PRINT)
    print(LIGHT)
    
    # Sortie log
    logging.info(PLEIN)
    logging.info(REQ + PRINT)
    logging.info(LIGHT)
    logging.info(REQ + STEP + "Déclenchement génération paramètres distants")

    # Appel de la fonction paramètres
    """ Géneration/récuperation des paramètres à déployer sur le client distant :
       le nouveau compte utilisateur : userID,
       son mot de passe : password
       l'adresse mac : mac 
       le hostname : host 
    """
    param = parametres(ip, REQ)
    password = str(param[0])
    userID = str(param[1])
    mac = str(param[2])
    host = str(param[3])

    # Sortie log	
    logging.info(LIGHT)
    logging.info(REQ + STEP + "Verification prérequis sécurité SSH")



	
    # Appel de la fonction sshpass
    """ Permet de déployer la clé publique du serveur sur le client distant 
        si cet échange n'a pas déjà été effectué, 
        si le statut retourné est error le traitement de ce client sera annulé
    """
    TXT = ""
    StatutSSHpass = sshpass(ip, TXT, mac, REQ)
    # Appel de la fonction sessionssh
    if (StatutSSHpass != "error"):
        logging.info(REQ + STEP + "Initialisation de la connexion ssh")
        # Ouverture de la session ssh sur le PC Distant + depot du script distant + ececution du script
        infoSystemDistant = sessionssh(ip, userID, password, REQ)
        separateur = " "
        system = separateur.join(infoSystemDistant.split(separateur)[-1:])

        # Initialisation des lignes des Inventaires
        dicoInventaires ={}
        dicoInventaires[InventaireUtilisateur] = str(now) + ";" + host + ";" + userID + ";" + password
        dicoInventaires[InventaireDomaine] = str(now) + ";" + host + ";" + mac + ";" + system
        for TypeInventaire,chaineInventaire in dicoInventaires.items():
            Inventaire(str(chaineInventaire), str(TypeInventaire), mac, REQ)

        # Création de la fiche Utilisateur
        FicheUtilisateur = CreationFicheUtilisateur(userID, password, host, REQ)
        if FicheUtilisateur != "":
            PRINT = INFO + "Création de la fiche utilisateur : " + str(FicheUtilisateur)
            print(PRINT)
            logging.info(REQ + PRINT)
        # Création de la fiche PC
        FichePC = QRcodePC(mac, host, REQ)
        if FichePC != "":
            PRINT = INFO + "Un nouveau QRcode PC a été généré : " + str(FichePC)
            print(PRINT)
            logging.info(REQ + PRINT)
        # Suppression des fichiers temporaires
        extension = "*.tmp"
        cleanWork(extension, REQ) 
        logging.info(REQ + OK + "Les fichiers temporaires " + extension + " ont été supprimés") 
		
# Affichage de l'arborescence
print(" ")
print(STEP + "AFFICHAGE ARBORESCENCE")
print(LIGHT)
os.system("tree " + DossierWork)
       
# Sortie console
print (" ")
print(PLEIN)
PRINT = STEP + 'TRAITEMENT TERMINE'
print(PRINT)
print(PLEIN)
print("")

# Sortie log
logging.info(PLEIN)
logging.info(PRINT)
logging.info(PLEIN)
 
