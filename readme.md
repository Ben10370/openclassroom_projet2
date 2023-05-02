# OpenClassroom_projet2: Web-scrapping

## Description

- article 1

Il s'agit d'un script de scraping Web écrit en Python. Le script récupère le site Web [https://books.toscrape.com/] pour extraire les données du livre, y compris le titre du livre, le prix, la disponibilité, la description du produit, la catégorie et l'image.

- article 2

Le script peut être exécuté pour récupérer les données de tous les livres sur le site Web ou pour une catégorie spécifique. Il crée un fichier CSV distinct pour chaque catégorie. Il télécharge et enregistre également les images de couverture des livres dans un répertoire séparé de chaques catégories.

## Prérequies

Ce script à été créer avec **_python version 3.8.10_** sur **_UBUNTU_**

Les **modules nécéssaires** sont:

**_beautifulsoup4==4.11.1_**
**_requests==2.28.2_**

## Installation

- étape 1 :

Avant de commencer, **cloner le projet en local sur votre machine**, **copiez l'URL de ce repo** et **lancez la commande suivante dans votre terminal**:

`git clone https://github.com/Ben10370/openclassroom_projet2.git` **(HTTPS)**

- étape 2 :

    - étapes 2.1

        Créer et activer l'environnement virtuel.

        Pour **créer** un environnement virtuel, **dans la racine du projet**, ouvrez votre terminal **exécutez la commande**: 
        
        `python -m venv <nom de l'environnement>`

        Pour **activer** l'environnement virtuel, **exécutez la commande**:
        
        `source env/bin/activate` 

À ce stade, votre terminal ajoutera probablement le nom de votre environnement au début de chaque ligne de votre terminal. 

Si vous exécutez `pip freeze`, vous ne devriez maintenant pas voir de module répertorié, cela montre qu'aucun module n'est installé dans votre environnement virtuel. C'est le comportement par défaut lorsque vous créez un environnement virtuel.

- étape 3 :

taper `cd` dans le répertoire où se trouve **_requirements.txt_** et dans votre terminal tapez la commande `pip install -r requirements.txt`

- étape 4 :

exécuter le code d'application : 

Dans la racine du projet, dans votre terminal tapez `python main.py` ou dans le cas ou vous utilisez python 3, taper `python3 main.py` pour que la magie commence

Si vous deviez **_quitter_** » ou **_désactiver_** votre environnement virtuel, exécutez la commande `deactivate` pendant que votre environnement virtuel est activé. Selon le terminal que vous utilisez, le suffixe (env) n’apparaîtra plus.

## Format des donnés

Une fois le script executé correctement, les fichiers suivants seront apparus le dossier de travail :

1. Un fichier CSV par catégorie d'ouvrages, nommé _nom_de_la_categorie_.csv, utilisant la virgule comme séparateur et contenant les informations suivantes, indiquées en en-tête du fichier :

* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url

2. Un fichier JPG par ouvrage, correspondant à l'image de sa couverture présente sur le site.
A noter que pour des raisons techniques d'enregistrement des fichiers, le nom de ces fichiers images correspond au titre de l'ouvrage et classées dans des sous dossiers qui portent le nom_de_la_categorie et ayant subi les modifications suivantes :

* Les caractères spéciaux suivants ont été remplacés par le caractère "_" :

* ’
  * '
  * :
  * .
  * &
  * \*
  * /
  * \\
  * ?

## Credits

Projet réalisé par Benoit BONNIVARD
Assisté par Idriss Nicolas (Mentor Openclassrooms)