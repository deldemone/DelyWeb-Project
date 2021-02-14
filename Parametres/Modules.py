#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
=============================
		LES MODULES
=============================
Nom :	Modules.py
Description : Ici sont référencées tous les modules appelées par les scripts RenewDomain.py, Variables.py et Fonctions.py
"""
__author__ = "Delphine Durand"
__version__ = "1.0.0"
__email__ = "contact@DelyWeb.fr"
__status__ = "Production"


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