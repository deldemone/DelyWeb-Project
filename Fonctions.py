#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
=============================
		LES FONCTIONS
=============================
Nom : Fonctions.py			 
Description : Ici sont référencées toutes les fonctions appelées par le script RenewDomain.py
"""

##################################################################################################################
__author__ = "Delphine Durand"
__version__ = "1.0.0"
__email__ = "contact@DelyWeb.fr"
__status__ = "Production"


### Chargement des fonctions et des modules
from Modules import *
from Variables import *



"""""""""""""""""""""""""""""""""""""""""""""""""""
			ENVIRONNEMENT DE TRAVAIL 
"""""""""""""""""""""""""""""""""""""""""""""""""""

#	INITIALISATION DES REPERTOIRES SI NON EXISTANT
""" Vérification de l'existance des répertoires utiles et création si non existant """
def checkRepertoireExistance(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
			# Sortie log
            logging.info(OK +  "Création " + path)
        except CreatePathError as e:
			# Sortie log
            logging.error(KO + e)
    else:
        MSG = OK + path + " existant"
		# Sortie log
        logging.info(MSG)

#	INITIALISATION DES FICHIERS SI NON EXISTANT
""" Vérification de l'existance des répertoires utiles et création si non existant """
def checkFileExistance(cle, fic):
    if not os.path.isfile(fic):
        try:
            fichier= open(fic, 'w')
            fichier.write(cle + "\n")	
			# Sortie log
            logging.info(OK + "Création " + fic)
            fichier.close()
        except Exception as e:
			# Sortie log
            logging.error(REQ + KO + str(e))
    else:
        MSG = OK + fic + " existant"
        logging.info(MSG)    

#	RéINITIALISATION DU REPERTOIRE FICHES UTILISATEUR
""" Suppression des anciennes fiches utilisateur """
def cleanfiche(repertoire):
    try:
        files = os.listdir(repertoire)
		# Sortie log
        logging.info(OK + "Suppression anciennes fiches utilisateur")
        for filename in os.listdir(repertoire) :
            os.remove(repertoire + "/" + filename)
            
    except:
		# Sortie log
        logging.error(Ko + "PB de Réinit. répertoire fiche utilisateur")

"""""""""""""""""""""""""""""""""""""""""""""""""""
			FONCTION OUTIL & PARAMETRES
"""""""""""""""""""""""""""""""""""""""""""""""""""

#	FONCTION DE GENERATION DE CHAINE ALEATOIRE
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

#	FONCTION NETTOYAGE	
def cleanWork(extension, REQ):
    """ Suppression des fichiers suivants leur extension"""
    try:
        for fichier in glob.glob(extension):
            os.remove(fichier)
    except Exception as e:
		# Sortie log
        logging.error(REQ + KO + str(e))   
		

#	FONCTION GENERATION/RECUPERATION DE PARAMETRES	
def parametres (ip, REQ):
    countError = 0
# Récuperation de l'adresse mac
    mac = ""
    try:
        writemac = os.system("arp -a " + ip + " | awk -F\" \" '{print $4}'> mac.tmp")
        mon_fichiermac=open("mac.tmp","r")
        mactmp = str(mon_fichiermac.read())
        mac = mactmp.rstrip("\n")   
    except:
	    # Sortie log
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
		# Sortie log
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
		# Sortie log
        logging.info(REQ + OK + "Génération des paramétres")
        return password, NewUser, mac, host
    else:
		# Sortie console
        PRINT = KO + "lors de la génération des paramétres"
        print(PRINT)
		# Sortie log
        MSG = REQ + PRINT
        logging.info(MSG)


"""""""""""""""""""""""""""""""""""""""""""""""""""
		FONCTION DE CONNEXION DISTANTE
"""""""""""""""""""""""""""""""""""""""""""""""""""

#	FONCTION SSHPASS
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
			# Sortie log
            logging.info(REQ + OK + "La clé du serveur déja présente sur client")
            present = True
            statut = "MacPresentInventaire"
            break
    if (present == False):
		# Sortie log
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

#	FONCTION SESSION SSH
def sessionssh(ip, userID, password, REQ):
    """ la session ssh se déroule en 3 étapes séquentielles qui dépendent de la bonne éxecution de la précédente
        la connexion ssh entre le serveur et le PC distant
        la connexion sftp avec depôt du script deploy.py sur le PC distant
        execution du script distant
    """
    system = ""
	#ouverture de la session ssh
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
    # ouverture de la session sftp et copy du script de deploiement
    if (sshsuccess == True):
        try:
			# Sortie log
            logging.info(LIGHT)
            logging.info(REQ + STEP + "Dépôt du script via le SFTP")
            sftp = ssh.open_sftp()
            sftp.put('/partage/deploy.py', '/tmp/deploy.py')
			# Sortie log
            logging.info(REQ + OK + "Dépôt du script python sur le client")
            sftp.close()
            sftpsuccess = True
            print(OK + "Déploiement du script sur le client")
        except Exception as e:
            print(e)
			# Sortie log
            logging.error(KO + str(e))
            sftpsuccess = False
        # exécution du script de déploiement
        if (sftpsuccess == True):
            try:
				# Sortie log
                logging.info(LIGHT)
                stdin, stdout, stderr = ssh.exec_command('python3 /tmp/deploy.py --userID ' + userID + ' --pwd ' + password)
                for line in stdout.read().splitlines():
                    sortieDist = (line.decode("utf-8", "ignore"))
                    #print("sortiedist = " + sortieDist)
                    if sortieDist != "" and "System" not in sortieDist:
						# Sortie console
                        print(sortieDist)
						# Sortie log
                        logging.info(REQ + sortieDist)
                    if "System" in sortieDist:
                        system = sortieDist
				# Sortie log
                logging.info(REQ + OK + "Exécution du script de déploiement terminée")
            except Exception as e:
				# Sortie console
                print(e)
				# Sortie log
                logging.error( KO + str(e))
                success = False	
    try:
        ssh.close()
		# Sortie log
        logging.info(REQ + OK + "Fermeture de la session ssh")   
    except Exception as e:
		# Sortie console
        print(e)
		# Sortie log
        logging.error(REQ + KO + str(e))
    logging.info(LIGHT)
    return system    


""" GENERATION DES FICHIERS DE SORTIE """

#	FONCTION DES INVENTAIRES 
def Inventaire(LigneInvent, typeInvent, mac, REQ):
    try:
        OpenInventaire = open(typeInvent,"r")	# ouverture de l'inventaire en lecture
        lignesInvent = OpenInventaire.readlines()
        Present = False
        for ligne in lignesInvent:		
            if mac in ligne:
                Present = True
        if Present == False:
			# Sortie log
            logging.info(REQ + STEP + "Inscription dans "+ typeInvent)
            writeInvent = open(typeInvent,"a")	# ouverture de l'inventaire en écriture
            writeInvent.write(LigneInvent + "\n")	# édition de l'inventaire
            writeInvent.close()		# fermeture du fichier inventaire
            logging.info(REQ + OK + "Nouvelle entrée dans l'inventaire :")
            logging.info(REQ + OK + typeInvent)
        else:
			# Sortie log
            logging.info(REQ + OK + "Entrée déjà présente dans inventaire :")
            logging.info(REQ + OK + typeInvent)
    except:
		# Sortie log
        logging.info(REQ + KO + "Aucune inscription possible dans l'inventaire :")
        logging.info(REQ + OK + typeInvent)
#	CREATION FICHE UTILISATEUR			
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
            fichier.write("	Login User	=	" + userID + "\n")
            fichier.write("	Mot de passe	=	" + password + "\n \n")
            fichier.write("\n" + PLEIN + "\n \n")
            fichier.close()
            logging.info(REQ + OK + "Création de la fiche " + userID)
            return fiche
        except:
			# Sortie log
            logging.info(REQ + KO + "Lors de l'édition de la fiche utilisateur")
    except:
		# Sortie log
        logging.info(REQ + KO + "Lors de la création de la fiche utilisateur")
		
#	CREATION FICHE PC = QRCODE			   
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
			# Sortie log
            logging.info(REQ + OK + "Création de la fiche " + NameJPGMac)
            return FilePath
        except Exception as e:
			# Sortie log
            logging.error(REQ + KO + str(e))
    else:
		# Sortie log
        logging.info(REQ + OK + NameJPGMac + " existant sous : ") 
        logging.info(REQ + OK + RepertoireFichePC)
        FilePath=""
        return FilePath
	