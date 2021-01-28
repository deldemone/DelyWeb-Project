#!/usr/bin/python3
# -*- coding: utf-8 -*-

###Description: Permet de scanner le reseau d'un domaine et de parametrer les clients à distance"""
##################################################################################################################
__author__ = "Delphine Durand Demongeot"
__version__ = "1.0.0"
__email__ = "dd0275416@gmail.com"
__status__ = "En cours de rédaction"

import os
import shutil



# Suppression de l'ancien stagiaire de son home
readPasswd = open("/etc/passwd", "r")	# ouverture du fichier utilisateur en lecture seule
lignes = readPasswd.readlines()
def suppOldUser():
    for ligne in lignes:
        if "mast" in ligne:
            separateur = ":"
            usOld = separateur.join(ligne.split(separateur)[0:1])
            print("Un user à supprimer : " + str(usOld))
            cmd = "userdel -f " + usOld
            try:
                os.system(cmd)
                MSG = " ### SUCCESS -Ancien utilisateur " + usOld + " a été supprimé."
                print(MSG)
                shutil.rmtree("/home/" + usOld)
                MSG = " ### SUCCESS -home de l'ancien utilisateur " + usOld + " a été supprimé."
                statut = "success"
                print(MSG)
                statut = "success"
                break
            except Exception as e:
                print(e)
                print(" ### Un pb est survenu lors de la suppression ancien user")
                statut = "error"

suppOldUser()