

#  Nom : Application  sur la génération de  ebillet 

## Description:  Cette application Flask est une plateforme de gestion d'offres et de billetterie électronique avec des fonctionnalités pour utilisateurs et administrateurs.


## Prérequis :

    Pour exécuter cette application Flask, voici les prérequis nécessaires :

Python 3.6 ou une version supérieure.
Modules Python :
* Flask
* Flask-SQLAlchemy
* Flask-Hashing
* psycopg2-binary (pour l'intégration avec PostgreSQL)
* WTForms (pour les formulaires)
* Flask-WTF (pour la validation des formulaires)



Pour installer les dépendances :

pip install -r requirements.txt

Base de Données :

Il faut installé et configuré sur votre machine  PostgreSQL, et  créer une base de données PostgreSQL pour  faire fonctionnée l’application.


Configuration de l’environnement  de developpement 
* Il faut créer un fichier .env ou configurez les variables d'environnement nécessaires pour les paramètres de la base de données et les clés secrètes.


 La structure des Répertoires :

Projet
app.py
requirements.txt
index.html
etc...

Static
qrcode
models
models.py
forms

Fonctionnalités
Liste des fonctionnalités principales pour l’application,
Créer et gérer des offres solo, duo et familiales
Interface utilisateur intuitive


Lancement de l'Application :
   Pour lancer l'application, exécutez la commande suivante dans le répertoire racine de votre projet :
cd nom du projet 
source  ./venv/bin/activate
flask  --app app run
En suivant ces prérequis, vous devriez pouvoir installer et exécuter l'application Flask correctement.





Auteurs
*  Développeur principal    Luyola matondo ridy   - git madondbi



