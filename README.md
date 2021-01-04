# PureBeurre
OC Projet 5
## About.
PureBeurre is the result of my project 5 on the OpenClassRooms path of application developer: Python.
It's an application that suggest a substitute for a chosen food product using data from the OpenFoodFacts API.
## Installation and requirements.
It requires Python 3, mysql-server and mysql-client version 8, and modules listed in the requirements.txt file.
### Install Python 3.
Link to the official web site : *[Download Python](https://www.python.org/downloads/)*
### Install MySQL.
Link to the official documentation : *[Install MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/)*
### Install PureBeurre.
Link to the GitHub repository : *[PureBeurre](https://github.com/screw-pack/PureBeurre.git)*<br><br>
- Fork the project : *[Fork a project](https://guides.github.com/activities/forking/)*<br>
- Create a directory for the clone.<br>
- Clone : <br><br>`user@computer:~/_path_/$ git clone <repository_url>`<br><br>
- Create a virtual environment : <br><br>`user@computer:~/_path_/$ python3 -m venv <environment_name>`<br>
### Install Python's modules.
- Activate the virtual environment : <br><br>`user@computer:~/_path_/$ source <environment_name>/bin/activate`<br><br>
- Install requirements : <br><br>`(.env) user@computer:~/_path_/$ pip install -r requirements.txt`<br>
## Create database.
- To create the database, just replace the values in the config.ini file with yours.<br><br>
`[mysql]`<br>
`host = localhost`<br>
`database = <your DB name>`<br>
`user = <your user name>`<br>
`password = <your password>`<br><br>
- Then in VENV, execute dbcreate.py file : <br><br>`(.env) user@computer:~/_path_/$ python dbcreate.py`<br>
## The App.
The user interface opens in a console.
The functionalities are accessible through a numbered menu.
The user accesses it by entering the corresponding number.
### Main menu.
- 1. Choisir une catégorie d'aliments : brings to a categories sub menu.
- 2. Retrouver mes aliments substitué : Displays the list of previously saved comparisons.
- 0. Quitter : quit the application.
### Categories menu.
Displays 10 products categories ordered by food groups. <br>
0 allows the user to return to the main menu.
### Products menu.
The system offers a selection of 10 products corresponding to the selected category.
These products are numbered, the user enters the associated number. <br>
0 allows the user to return to the main menu.
### Substitut.
The system displays a substitute food (in detail) for the selected product.
And it asks the user if they want to save this comparison. <br>
- 1. Oui : the products and its substitute are both saved in the database.<br>
- 0. Non. Retour au menu principal : the user returns to the main menu.
### Substituted food menu.
The system displays the previously saved comparisons.
These comparisons are numbered, the user has the option to enter a number to see the details of the products and its substitut.<br>
0 allows the user to return to the main menu.
