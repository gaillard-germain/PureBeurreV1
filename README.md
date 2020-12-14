# PureBeurre
OC Projet 5
## Qu'est-ce que c'est.
PureBeurre est le résultat de mon projet 5 sur le parcours OpenClassRooms de développeur d'application : Python.
C'est une application qui propose un substitut à un aliment choisit en utilisant les données de l'API OpenFoodFacts.
## Installation et Prérequis.
Requiert l'installation de Python 3.8, mysql-server et mysql-client version 8, et des modules listés dans le fichier requirements.txt.
### Installer Python 3.8.
Le lien vers le site officiel : *[Télécharger Python](https://www.python.org/downloads/)*
### Installer MySQL.
Le lien vers la documentation officiel : *[Installer MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/)*
### Installer PureBeurre.
Le lien vers le dépot GitHub : *[PureBeurre](https://github.com/screw-pack/PureBeurre.git)*<br><br>
- Forker le projet : *[Forker un projet](https://guides.github.com/activities/forking/)*<br>
- Créer un dossier pour stocker le clone de votre fork.<br>
- Cloner : <br><br>`user@computer:~/chemin/$ git clone <votre dépot du fork>`<br><br>
- Créer un environnement Virtuel : <br><br>`user@computer:~/chemin/$ python3 -m venv <le nom de votre environnement>`<br>
### Installer les modules Python.
- Activer l'environnement virtuel : <br><br>`user@computer:~/chemin/$ source <nom de l'environnement>/bin/activate`<br><br>
- Installer les Prérequis : <br><br>`(.env) user@computer:~/chemin/$ pip install -r requirements.txt`<br>
## Créer la base de données.
- Pour créer la base de données il suffit de remplacer les valeurs du fichier config.ini par les votre.<br><br>
`[mysql]`<br>
`host = localhost`<br>
`database = <nom de la DB>`<br>
`user = <nom utilisateur>`<br>
`password = <mot de passe>`<br><br>
- Ensuite, dans votre VENV executer le fichier dbcreate.py : <br><br>`(.env) user@computer:~/chemin/$ python dbcreate.py`<br>
## L'application.
L'interface utilisateur s'ouvre dans une console.
Les fonctionnalités sont accessibles a travers un menu dont les choix sont numéroté.
L'utilisateur y accède en entrant le numéro correspondant.
### Menu principal.
- 1. Choisir une catégorie d'aliments : Renvoi à un sous menu catégories.
- 2. Retrouver mes aliments substitué : Affiche la liste des comparaisons sauvegardées précédemment.
- 0. Quitter : quitter l'application.
### Menu catégories.
Affiche les catégories d'aliments par groupes alimentaire de 1 à 10.<br>
0 permet à l'utilisateur de revenir au menu principal.
### Menu aliments.
Le système propose une sélection de 10 aliments correspondants à la catégorie sélectionnée.
Ces aliments sont numérotés, l'utilisateur rentre le numéro associé.<br>
0 permet à l'utilisateur de revenir au menu principal.
### Substitut.
Le système affiche un aliment de substitution (en détail) à l'aliment sélectionné.
Et il demande à l'utilisateur si il veut sauvegarder cette comparaison.<br>
- 1. Oui : l'aliment et son substitut sont sauvegardés dans la base de données.<br>
- 0. Non. Retour au menu principal : l'utilisateur revient au menu principal
### Menu aliments substitués.
Le système affiche les comparaisons préalablement sauvegardés.
Les aliments sont numérotés, l'utilisateur a la possibilité d'entrer un numéro pour voir les détails de l'aliment.<br>
0 permet à l'utilisateur de revenir au menu principal.
