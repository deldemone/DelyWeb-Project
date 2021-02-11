## Déroulement du script 

| Auteur | Delphine Durand |
| :------------ |:---------------:| 
| Date de création     | 18/01/2021 | 
| Dernière modification      | 06/02/2021       | 
| Version de Python | 3.7.3        |  

> Ci-dessous les étapes de déroulement du script

#### Step 1 :	Chargement Des Fonctions, Des Modules Et Des Variables
#### Step 2 :	Execution Du Script	

     """On récupère le niveau de log
| Niveau log | Description                    |
| ------------- | ------------------------------ |
|**`DEBUG`** |  Information détaillée, intéressante seulement lorsqu'on diagnostique un problème.       |
|**`INFO`** |  Confirmation que tout fonctionne comme prévu.      |
|**`WARNING`** |  L'indication que quelque chose d'inattendu a eu lieu, ou de la possibilité d'un problème dans un futur proche (par exemple « espace disque faible »). Le script fonctionne encore normalement.      |
|**`ERROR `** |  Du fait d'un problème plus sérieux, le logiciel n'a pas été capable de réaliser une tâche.    
|**`CRITICAL`** |  Une erreur sérieuse, indiquant que le programme lui-même pourrait être incapable de continuer à fonctionner. |


#### Step 3 :	Initialisation Du Log
#### Step 4 :	Preparation de l'environnement de travail

    """ Vérification de l'existance des répertoires utiles et création si non existant
        Vérification de l'existance des fichiers utiles et création si non existant
        Suppression des anciennes fiches utilisateur
    """
#### Step 5 :	Scanner Ip

    """ Le scanner ip fonctionne de la manière suivante :
    Il récupère le paramètre --réseau qui correspond au 3 premiers octets de la cible
    Si une range est définit il scannera uniquement l'étendue précisée 
    exemple : Python3 RenewDomain.py --reseau 192.168.122 --range 3,10
    La range par défaut est 2,254 """

#### Step 6 :	Traitement Client
#### Step 6.a :	Géneration du numéro de requête

    """ A chaque traitement de client nous générons un numero de reqête unique """

#### Step 6.b :	Géneration/récuperation des paramètres

    """Géneration/récuperation des paramètres à déployer sur le client distant :
       le nouveau compte utilisateur : userID,
       son mot de passe : password
       l'adresse mac : mac 
       le hostname : host 
    """
#### Step 6.C : Echange De Cle Serveur - Client

    """ La fonction verifie que l'adresse mac ne soit pas déjà référencé dans l'inventaire
        si cet échange n'a pas déjà été effectué, 
        => déploiement de la clé publique du serveur sur le client distant 
        si le statut retourné est error le traitement de ce client sera annulé.
    """
#### Step 6.D : Connexion SSH vers le client

    """ la session ssh se déroule en 3 étapes séquentielles qui dépendent 
	de la bonne  éxecution de la précédente :
        A. La connexion ssh entre le serveur et le PC distant
        B. La connexion sftp avec depôt du script deploy.py sur le PC distant
        C. L'execution du script deploy.py :
			1. Suppression de l'ancien userID
					On vérifie qu'un ancien utilisateur est reférencé
					Si présence d'un ancien utilisateur
					On ferme sa session et on le supprime
					On supprime également  son home
			2. Création du nouvel utilisateur
					Création du nouvel utilisateur
					Application du nouveau mot de passe complexe
					Changement du shell par défaut en bash
			3. Extraction des informations système
    """
#### Step 7.a : Valorisation De L'Inventaire Utilisateur
#### Step 7.b : Valorisation De L'Inventaire Du Parc
#### Step 8 : CréAtion De La Fiche Utilisateur
> User : USERSS006-1291

![](https://github.com/deldemone/DelyWeb-Project/blob/main/Documents/USERSS006-1291.PNG)
#### Step 9 : CréAtion De La Fiche Pc / Qrcode
> QRCode du PC mac : 08:00:27:ea:fa:15

![](https://github.com/deldemone/DelyWeb-Project/blob/main/Documents/080027eafa15.jpg)
#### Step 10 : Suppression Des Fichiers Temporaires
#### Step 11 : Affichage De La Nouvelle Arborescence

