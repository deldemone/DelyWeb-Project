#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Nom :			 RenewDomain.py

Exécution :		RenewDomain.py --debug info|warn|debug --reseau 192.168.122 --range 2,10

Action :		Permet de scanner le reseau d'un domaine 
				De parametrer les comptes utilisateurs à distance 
				De maintenir un inventaire du PARC INFORMATIQUE
				De créer des fiches utilisateurs (Login, mot de passe, hostname)
				De créer des QRcode à partir de l'adresse mac à apposer sur les postes de travail
"""
##################################################################################################################
__author__ = "Delphine Durand"
__version__ = "1.0.0"
__email__ = "contact@DelyWeb.fr"
__status__ = "Production"

### STEP 1 : Chargement des fonctions et des modules
from Fonctions import *
from Modules import *

### STEP 2 :	EXECUTION DU SCRIPT		
""" 
L'execution du script néccessite deux parémètres obligatoires
--log debug|info|warn
--reseau le réseau cible 
et un facultatif --range ipdebut,ipfin
"""
#=== LES PARAMETRES	D'APPEL DU SCRIPT		

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

#=== RECUPERATION DU NIVEAU DE LOG			

""" 
On récupère le niveau de log
DEBUG	:	Information détaillée, intéressante seulement lorsqu'on diagnostique un problème
INFO	:	Confirmation que tout fonctionne comme prévu.
WARNING	:	L'indication que quelque chose d'inattendu a eu lieu, ou de la possibilité d'un problème dans un futur proche 
(par exemple « espace disque faible »). Le script fonctionne encore normalement.
ERROR	:	Du fait d'un problème plus sérieux, le logiciel n'a pas été capable de réaliser une tâche.
CRITICAL:	Une erreur sérieuse, indiquant que le programme lui-même pourrait être incapable de continuer à fonctionner.
"""
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
#=== Exception niveau de log non défini
if ( nivLog == None ):
    raise ValueError('Niveau de log invalide, vous avez saisi : %s' % niveau + '\n usage : encours.py --log=debug|info|warn --reseau=192.168.1.0')

#=== FORMATAGE DE LIGNE DE LOG
logging.basicConfig(filename=FichierLOG, filemode='w', format='%(asctime)s ' + ' %(message)s', level=nivLog)

### STEP 3 :	INITIALISATION DU LOG				

logging.info(PLEIN)
logging.info(INTER + "     DEBUT EXECUTION DU SCRIPT    " + INTER)
logging.info(PLEIN)

### STEP 4 :	PREPARATION DE L'ENVIRONNEMENT DE TRAVAIL

#=== VERIFICATION ARBORESCENCE SERVEUR
logging.info(STEP +  "Contrôle arborescence")
logging.info(LIGHT)
for cle,path in dicoRepertoires.items():
    checkRepertoireExistance(path)

#=== VERIFICATION FICHIERS REQUIS
""" vérifcation que les fichiers requis sont existants, dans la négative Création de ces fichiers"""
logging.info(PLEIN)
logging.info(STEP +  "Contrôle des fichiers requis")
logging.info(LIGHT)
for cle,fic in dicoFichier.items():
    checkFileExistance(fic, cle)

#=== CREATION LIEN SYMBOLIQUE LOG	
os.system("ln -s " + FichierLOG + " " + DossierWork)

#=== SUPPRESSION ANCIENNES FICHES UTILISATEURS
repertoire = RepertoireFicheUtilisateur
cleanfiche(repertoire)

### STEP 5 :	SCANNER IP
""" Le scanner ip fonctionne de la manière suivante :
    Il récupère le paramètre --réseau qui correspond au 3 premiers octets de la cible
    Si une range est définit il scannera uniquement l'étendue précisée 
    exemple : Python3 RenewDomain.py --reseau 192.168.122 --range 3,10
    Le range par défaut est 1,254 """
#=== SORTIE CONSOLE
os.system('clear')
print(PLEIN)
MSG = STEP + 'Démarrage du scanner IP'
print(MSG)
print(LIGHT)

#=== SORTIE LOG
logging.info(PLEIN)
logging.info(MSG)

#=== RECUPERATION DES PARAMETRES D'APPEL SCRIPT

#=== Le --reseau 
reseau = args.reseau

#=== --range L'étendue cible si elle a été précisée
etenduecible = args.range

if args.range != "" :
    separateur = ","
    IPdebut = separateur.join(etenduecible.split(separateur)[:-1])
    IPfin = separateur.join(etenduecible.split(separateur)[1:])
else:
    IPdebut = 2
    IPfin = 254
    print (IPdebut + "<>" + IPfin)

#=== TABLEAU DES IP 
ipmachines = []
#=== SCAN DU RESEAU PLAGE IP [2-254] OU RANGE DEFINIE
for ping in range(int(IPdebut),int(IPfin)):
    if ( str(reseau) != ""):
        adresse = reseau + "." + str(ping)
        socket.setdefaulttimeout(1)
        try:
            hostname, alias, listadresse = socket.gethostbyaddr(adresse)
            #=== SORTIE CONSOLE
            PRINT = INFO + adresse + ' est actif sur le réseau'
            print(PRINT)
            #=== SORTIE LOG
            MSG = REQ + PRINT
            logging.info(MSG)
#=== EXCEPTION : AUCUN CLIENT CONNECTE AVEC IP 
        except socket.herror:
            hostname = None
            alias = None
            listadresse = adresse
#=== vALORISATION DU TABLEAU IP CONNECTEES
        if (hostname != None):
            ipmachines.append(adresse)
    else:
        exit("Merci de renseigner le sous-réseau à reinitialiser : exemple Python3 encours.py --log=debug 192.168.1.0")
if ipmachines == [] :
    #=== SORTIE CONSOLE
    PRINT = KO + "Aucun client sur la range : " + IPdebut + " <> " + IPfin
    print (PRINT)
    #=== SORTIE LOG
    MSG = REQ + PRINT
    logging.info(MSG)

### STEP 6 :	TRAITEMENT CLIENT

for ip in ipmachines:

    # STEP 6.a :	Géneration du numéro de requête sur 5 caractères avec prefixe REQ: Appel de la fonction aleatoireString
    """ A chaque traitement de client nous générons un numero de reqête unique"""
    nbcar = 5  
    type = "REQ"  
    REQ = aleatoireString(nbcar, type)

    # STEP 6.b : Initialisation du traitement
    #=== SORTIE CONSOLE
    print("")
    PRINT = STEP + "TRAITEMENT DE " + ip
    print(PRINT)
    print(LIGHT)
    
    #=== SORTIE LOG
    logging.info(PLEIN)
    logging.info(REQ + PRINT)
    logging.info(LIGHT)
    logging.info(REQ + STEP + "Déclenchement génération paramètres distants")

    # STEP 6.c : Appel de la fonction paramètres
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

    #=== SORTIE LOG
    logging.info(LIGHT)
    logging.info(REQ + STEP + "Verification prérequis sécurité SSH")
	
    # STEP 6.d : Appel de la fonction sshpass
    """ Permet de déployer la clé publique du serveur sur le client distant 
        si cet échange n'a pas déjà été effectué, 
        si le statut retourné est error le traitement de ce client sera annulé
    """
    TXT = ""
    StatutSSHpass = sshpass(ip, TXT, mac, REQ)
	
    # STEP 6.e :  Appel de la fonction sessionssh
    if (StatutSSHpass != "error"):
        
		#=== SORTIE LOG
        logging.info(REQ + STEP + "Initialisation de la connexion ssh")
        #=== Ouverture de la session ssh sur le PC Distant + depot du script distant + ececution du script
        infoSystemDistant = sessionssh(ip, userID, password, REQ)
        print("infoSystemDistant = " + infoSystemDistant)
        separateur = " "
        system = ""
        system = separateur.join(infoSystemDistant.split(separateur)[-1:])

        # STEP 6.f : Initialisation des lignes des Inventaires
        dicoInventaires ={}
        dicoInventaires[InventaireUtilisateur] = str(now) + ";" + host + ";" + userID + ";" + password
        dicoInventaires[InventaireDomaine] = str(now) + ";" + host + ";" + mac + ";" + system
        for TypeInventaire,chaineInventaire in dicoInventaires.items():
            Inventaire(str(chaineInventaire), str(TypeInventaire), mac, REQ)

        # STEP 6.g : Création de la fiche Utilisateur
        FicheUtilisateur = CreationFicheUtilisateur(userID, password, host, REQ)
        if FicheUtilisateur != "":
		    #=== SORTIE CONSOLE
            PRINT = INFO + "Création de la fiche utilisateur : " + str(FicheUtilisateur)
            print(PRINT)
			
        # STEP 6.h : Création de la fiche PC
        FichePC = QRcodePC(mac, host, REQ)
        if FichePC != "":
			#=== SORTIE CONSOLE
            PRINT = INFO + "Un nouveau QRcode PC a été généré : " + str(FichePC)
            print(PRINT)
			#=== SORTIE LOG
            logging.info(REQ + PRINT)
        # STEP 6.i : Suppression des fichiers temporaires
        extension = "*.tmp"
        cleanWork(extension, REQ) 
		#=== SORTIE LOG
        logging.info(REQ + OK + "Les fichiers temporaires " + extension + " ont été supprimés") 
		
# STEP 7 :  AFFICHAGE ARBORESCENCE
#=== SORTIE CONSOLE
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
 
