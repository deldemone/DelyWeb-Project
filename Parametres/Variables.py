#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
=============================
		LES VARIABLES
=============================
Nom :	Variables.py
Description : Ici sont référencées toutes les variables et dictionnaires appelés par les scripts RenewDomain.py et Fonctions.py

"""

__author__ = "Delphine Durand"
__version__ = "1.0.0"
__email__ = "contact@DelyWeb.fr"
__status__ = "Production"

### Chargement des modules
from Parametres.Modules import *


### VARIABLES GLOBALES

RetourFonctionAleatoireString = ""
now = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
NumSemaine = datetime.datetime.now().strftime("%U")

### LES REPERTOIRES
DossierWork = "/root/Work"
LOG = "/var/log"
RepertoireFicheUtilisateur = DossierWork + "/UserSemaine" + NumSemaine
RepertoireFichePC = DossierWork + "/QRcodePC"
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
