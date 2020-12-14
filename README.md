# PureBeurre  
OC Projet 5  
## Qu'est-ce que c'est.  
PureBeurre est le résultat de mon projet 5 sur le parcours OpenClassRooms de développeur d'application : Python.
C'est une application qui propose un substitut à un aliment choisit en utilisant les données de l'API OpenFoodFacts.  
## Installation et Prérequis.  
Requiert l'installation de Python 3.8, MySQL Connector, mysql-server et mysql-client version 8.  
### Installer Python 3.8.  
Le lien vers le site officiel : *[Télécharger Python](https://www.python.org/downloads/)*  
### Installer MySQL.  
Le lien vers la documentation officiel : *[Installer MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/)*  
### Installer PureBeurre.
Le lien vers le dépot GitHub : *[PureBeurre](https://github.com/screw-pack/PureBeurre.git)*  
Forker le dépôt : *[Forker un projet](https://guides.github.com/activities/forking/)*
Créer un dossier pour stocker le clone du dépôt.
Cloner : `user@computer:~/chemin/$ git clone <votre dépot du fork>`  
Créer un environnement Virtuel : `user@computer:~/chemin/$ python3 -m venv <le nom de votre environnement>`  
### Installer MySQL Connector.
Activer l'environnement virtuel : `user@computer:~/chemin/$ source <nom de l'environnement>/bin/activate`  
Installer les Prérequis : `(.env) user@computer:~/chemin/$ pip install -r requirements.txt`  
## Créer la base de données.  
Pour créer la base de données il suffit de remplacer les valeurs du fichier config.ini par les votre.  
`[mysql]`  
`host = localhost`  
`database = <nom de la DB>`  
`user = <nom utilisateur>`  
`password = <mot de passe>`  
Dans le VENV executer le fichier dbcreate.py : `(.env) user@computer:~/chemin/$ python dbcreate.py`  
## L'application.  
L'interface utilisateur s'ouvre dans une console.
