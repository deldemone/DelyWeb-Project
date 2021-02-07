#!/usr/bin/python3
# -*- coding: utf-8 -*-

###Description: Script de déploiement"""
##################################################################################################################
__author__ = "Delphine Durand Demongeot"
__version__ = "1.0.0"
__email__ = "dd0275416@gmail.com"
__status__ = "En cours de rédaction"


########################################################################
####################		LES MODULES			
########################################################################

import os
import shutil
import argparse
import sys
import platform

########################################################################
####################		LES VARIABLES			
########################################################################

# CADRE & PREFIXE LOG
OK = " ##  OK  ## *** DIST - "
KO = " ##  KO  ## *** DIST - "
SO = " ##  SO  ## *** DIST - "
INFO = " ## INFO ## *** DIST - "
STEP = " ## STEP ## *** DIST - "

#===================================================#
#	LES PARAMETRES			
#===================================================#  

""" L'execution du script néccessite deux parémètres obligatoires
--userID le nouveau login
--pwd le mot de passe de l'utilisateur
"""
parser = argparse.ArgumentParser('Executer ce script requiert deux arguments --userID et --pwd ')

parser.add_argument('--userID',
                    type=str,
                    help='Préciser le nouvel utilisateur ex : --userID STG04',
                    required=True)
parser.add_argument('--pwd',
                    type=str,
                    help='--pwd votremdp',
                    required=True)
args = parser.parse_args()

#Récuperation des paramètres
userID = args.userID
password = args.pwd

########################################################################
####################		LES FONCTIONS			
########################################################################

def suppOldUser():
    """ On vérifie qu'un ancien utilisateur est reférencé
        Si présence d'un ancien utilisateur
        On ferme sa session et on le supprime
        On supprime également  son home
    """
    readPasswd = open("/etc/passwd", "r")
    lignes = readPasswd.readlines()
 
    PresenceOldUser = False
    for ligne in lignes:
        if "USERS0" in ligne:
            separateur = ":"
            userOld = separateur.join(ligne.split(separateur)[0:1])
            print(OK + "Un user à supprimer : " + str(userOld))
            cmd = "pkill -u "  + userOld + " ; userdel -f " + userOld
            try:
                os.system(cmd)
                print(OK + "Fermeture session " + userOld + ".\n" + OK + "Ancien utilisateur " + userOld + " a été supprimé.")
                shutil.rmtree("/home/" + userOld)
                PresenceOldUser =  True
                print(OK + "/home de l'ancien utilisateur " + userOld + " a été supprimé.")
                break
            except Exception as e:
                print(e)
                print(KO + "Un pb est survenu lors de la suppression ancien user")
    if ( PresenceOldUser == False ):
        print(SO + "-Aucun ancien utilisateur à supprimer.")

# Création du nouvel utilisateur et de son home
def addNewUser(userID, password):
    """ Création du nouvel utilisateur
        Application du nouveau mote de passe complexe
        Changement du shell par défaut en bash
    """
    try:
        cmd = 'useradd -m ' + userID + '; echo \"' + userID + '\":' + password + ' | chpasswd ; chsh -s /bin/bash ' + userID 
        os.system(cmd)
        print(OK + "Nouvel utilisateur " + userID + " a été créé.\n" + OK + "/Home " + userID + " a été créé.\n" + OK + "PWD sécurisé déployé pour " + userID + ".\n" + OK + "Changement du shell par défaut en bash")
    except Exception as e:
        print(e)
        print(KO + "Un pb est survenu lors de la suppression ancien user")



########################################################################
####################		APPEL DES FONCTIONS			
########################################################################
print(STEP + "Exécution du script de déploiement")
suppOldUser()
addNewUser(userID, password)
# Extraction des informations système
print(INFO + "System = " + str(platform.platform()))
