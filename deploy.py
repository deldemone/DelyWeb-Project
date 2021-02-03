#!/usr/bin/python3
# -*- coding: utf-8 -*-

###Description: Script de déploiement"""
##################################################################################################################
__author__ = "Delphine Durand Demongeot"
__version__ = "1.0.0"
__email__ = "dd0275416@gmail.com"
__status__ = "En cours de rédaction"

import os
import shutil
import logging
import argparse

##################################################################################################################
#	Définition des arguments
#=======================================================#

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

userID = args.userID
password = args.pwd
OK = " ##  OK  ## *** DIST - "
KO = " ##  KO  ## *** DIST - "
SO = " ##  SO  ## *** DIST - "
INFO = " ## INFO ## *** DIST - "
STEP = " ## STEP ## *** DIST - "
# Suppression de l'ancien stagiaire et de son home
readPasswd = open("/etc/passwd", "r")	# ouverture du fichier utilisateur en lecture seule
lignes = readPasswd.readlines()
def suppOldUser():
    PresenceOldUser = False
    for ligne in lignes:
        if "STGS" in ligne:
            separateur = ":"
            userOld = separateur.join(ligne.split(separateur)[0:1])
            MSG = OK + "Un user à supprimer : " + str(userOld)
            logging.info(MSG)
            cmd = "pkill -u "  + userOld + " ; userdel -f " + userOld
            try:
                os.system(cmd)
                MSG = OK + "Fermeture session " + userOld + ".\n" + OK + "Ancien utilisateur " + userOld + " a été supprimé."
                print(MSG)
                logging.info(MSG)
                shutil.rmtree("/home/" + userOld)
                MSG = OK + "/home de l'ancien utilisateur " + userOld + " a été supprimé."
                PresenceOldUser =  True
                print(MSG)
                logging.info(MSG)
                break
            except Exception as e:
                print(e)
                print(KO + "Un pb est survenu lors de la suppression ancien user")

    if ( PresenceOldUser == False ):
        MSG = SO + "-Aucun ancien utilisateur à supprimer."
        print(MSG)
        logging.info(MSG)


# Création du nouvel utilisateur et de son home
def addNewUser(userID, password):
    try:
        cmd = 'useradd -m ' + userID + '; echo \"' + userID + '\":' + password + ' | chpasswd ; chsh -s /bin/bash ' + userID 
        os.system(cmd)
        MSG = OK + "Nouvel utilisateur " + userID + " a été créé.\n" + OK + "/Home " + userID + " a été créé.\n" + OK + "PWD sécurisé déployé pour " + userID + ".\n" + OK + "Changement du shell par défaut en bash"
        print(MSG)
    except Exception as e:
        print(e)
        print(KO + "Un pb est survenu lors de la suppression ancien user")
		
print(STEP + "Exécution du script de déploiement")

suppOldUser()
addNewUser(userID, password)
