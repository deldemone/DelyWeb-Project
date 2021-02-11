**Script python d'automatisation de Configuration de poste client & de Gestion de Parc informatique**
-------------  -------------

| Auteur | Delphine Durand |
| :------------ |:---------------:| 
| Date de création     | 18/01/2021 | 
| Dernière modification      | 06/02/2021       | 
| Version de Python | 3.7.3        |  

Créé sur Linux pour environnement Linux      
-------------  -------------



### Contexte
> Ce script est un cas d'étude.
Il a été codé dans le cadre du projet 6 : Participez à la vie de la communauté Open Source de la formation d'Administrateur Infrastructure et Cloud de chez OpenClassrooms. La mission était de créer un script permettant d'automatiser des tâches d'administration et de partager ce code avec la communauté sur un répertoire personnel GitHub.

### Description
> Dans le cadre de l'association "A fond Linux", nous sommes amenés chaque fin de semaine à reinitialiser tous les postes du parc informatique et de les préparer pour l'arrivée de nouveaux apprenants.
Ce script permet d'automatiser la configuration de ces postes à distance via le SSH (création nouveau user, mdp complexe, suppression ancien user, repertoire, changement de bash en shell).
Il permet également de maintenir un inventaire du parc informatique ainsi que de créer des QRcode destinés à être apposé sur chaque poste.
Ce script peut être appelé manuellement ou via un cron defini dans le crontab.


### Le crontab
> Dans le cadre de cette association, nous planifions cette tâche le premier jour de la semaine soit le dimanche à 17h00 via le crontab :

**`crontab -e`**

**`0 17 * * 0 python3 /root/RenewDom/RenewDomain.py --log info --reseau 192.168.122 --range 3,254`**


### Les prérequis
-------------  -------------
> Dans un premier temps il vous faudra renseigner le mot de passe administrateur de vos postes clients dans le fichier .pwd à la racine du dépôt.

### Configuration du serveur  
#### Les packets 

| Packets| Commande                    |
| ------------- | ------------------------------ |
|**`Git`** | `sudo apt install git -y`**     |
|**`Tree`** |  `sudo apt install tree -y`**      |
|**`Serveur SSH `** |  `sudo apt-get install openssh-server -y` |
> A noter : Pour les versions RedHat utiliser yum au lieu de apt 

#### Importation du projet depuis Github

| Etape| Commande                    |
| ------------- | ------------------------------ |
|**`Initialisation du répertoire local du serveur`** | `sudo git init`     |
|**`Faire pointer le dépôt local pointe sur le dépôt distant`** |  `sudo git remote add US https://github.com/deldemone/DelyWeb-Project.git`    |
|**`Clonez le dépôt et le dupliquer en local `** |  `sudo git clone https://github.com/deldemone/DelyWeb-Project.git` |


#### Le SSH
> A noter : L'authentification se fera par échanges de clés publique/privée

##### Génération des clés SSH  **`ssh-keygen`**

#### Installation des modules
| Module| Commande                    |
| ------------- | ------------------------------ |
|**`pip Python`** | `$  sudo apt install python3-pip`      |
|**`Paramiko`** |  `$  sudo pip3 install paramiko`       |
|**`qrcode et de pillow `** |  `$  sudo pip3 install qrcode[pil]` |
> A noter : Pour les versions RedHat utiliser yum au lieu de apt

#### Configuration des postes cibles
> Chaque poste de travail devra porter un nom hostname unique, et disposer d'un compte administrateur accessible par SSH
Afin d'autoriser l'utilisateur root à se connecter en SSH :
Il faudra donc installer opensshserver 
Décommenter la ligne du fichier */etc/ssh/sshd.config *et mettre «yes»

**`PermitRootlogin yes`**
> Il faudra également installer python3-pip

-------------  -------------
### Description basique des modules utilisés

| Modules | Description                    |
| ------------- | ------------------------------ |
|**`sys`** |  Module accès aux paramètres et fonctions propres aux systèmes.       |
|**`socket`** |  Module communication réseau.       |
|**`os`** |  Module système d'exploitation.       |
|**`logging`** |  Module de journalisation.       |
|**`argparse`** |  Module d'analyse de ligne de commande.       |
|**`random`**|  Module génèration des nombres pseudo-aléatoires.       |
|**`from string  punctuation, ascii_letters, digits, ascii_uppercase`** |  Module des opérations usuelles sur les chaînes.       |
|**`datetime`** |  Module format date & heure.       |
|**`paramiko`**|  Module permettant de programmer l'envoi de commandes à un équipement réseau via le protocole SSH.       |
|**`qrcode`**|  Module permettant de génèrer des QRCode.       |
|**`from PIL  ImageDraw, Image, ImageFont`**|  Mmodule permettant la manipulation des images QRcode.       |
|**`glob`**|  Module utilisé pour manipulation des extensions.       |

-------------  -------------
### Les fichiers INPUT
| Nom | Description                    |
| ------------- | ------------------------------ |
|**`Fonctions.py`** |  Référencement de toutes les fonctions appelées par le script RenewDomain.py.       |
|**`Modules.py`** |  Référencement de tous les modules appelées par les scripts RenewDomain.py, Variables.py et Fonctions.py.       |
|**`Variables.py`** |  Référencement de toutes les variables et dictionnaires appelés par les scripts RenewDomain.py et Fonctions.py.       |
|**`.pwd `** |  Fichier securité mot de passe root.       |

-------------  -------------
### Les fichiers OUTPUT
Des exemples de chaque type se trouve dans [Lien documents](https://github.com/deldemone/DelyWeb-Project/tree/main/Documents)
| Nom | Path                    |
| ------------- | ------------------------------ |
|**`Le LOG`** |  /root/Work/RenewDomain.log -> /var/log/RenewDomain.log (lien symbolique).       |
|**`L'inventaire utilisateur`** |  /root/Work/Inventaire/InventaireUtilisateurS0X.       |
|**`L'inventaire du parc`** |  /root/Work/Inventaire/InventaireDomaine.       |
|**`Les fiches utilisateurs `** |  /root/Work/UserSemaine0X/USERS00X-XXXX.    
|**`Les QRcode`** |  /root/Work/QRcodePC/mac.jpg.  

-------------  -------------
### Execution du script et  arguments
Exemple :
**`RenewDomain.py --log info|warn|debug --reseau 192.168.122 --range 2,10`**

> L'execution du script néccessite deux paramètres **obligatoires**
\-\-log debug|info
\-\-reseau les 3 premiers octets du réseau cible 
et un paramètre **facultatif** \-\-range ipdebut,ipfin <= derniers octets
-------------  -------------
### Déroulement du script : [Lien déroulement](https://github.com/deldemone/DelyWeb-Project/blob/main/Documentation.md)
-------------  -------------
### Sortie Console
![](https://github.com/deldemone/DelyWeb-Project/blob/main/Documents/SortieConsole.PNG)

-------------  -------------
### Conclusion  et Contribution
> Ce script est un cas d'étude.
Néanmoins il y a quelques fonctions interressantes qui pourraient aider la communauté apprenantes. 

> Ces fonctions sont contenues dans le fichier Fonctions.py :

> - Fonctions intervenants sur les répertoires et les fichiers dans la partie "Environnement de travail"
> - Quelques fonctions outils (génération de chaines aléatoires, nettoyage de repertoire suivant les extensions de fichiers, etc)
> - Fonctions relatives aux connexions distantes via le SSH
> - Fonctions de création de QRCode

>N'hésitez pas à me soumettre vos contributions, je suis très réactive.
> https://docs.microsoft.com/fr-fr/learn/modules/contribute-open-source/3-contribute

## Version:  
1.0

## License:  
#### GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

