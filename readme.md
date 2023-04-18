OpenClassroom_projet2: Web-scrapping

Il s'agit d'un script de scraping Web écrit en Python. Le script récupère le site Web " https://books.toscrape.com/ " pour extraire les données du livre, y compris le titre du livre, le prix, la disponibilité, la description du produit, la catégorie et l'image.

Le script contient plusieurs fonctions qui exécutent des tâches spécifiques. La "download_image" fonction télécharge l'image de couverture du livre et la stocke localement. La "scrap_book" fonction extrait les données d'un livre à partir d'une seule page de livre. La "write_book_data_csv" fonction écrit les données du livre dans un fichier CSV. La "scrap_category" fonction récupère toutes les URL de livres à partir d'une seule page de catégorie. La "get_category_name_from_url" fonction extrait le nom de la catégorie de l'URL de la catégorie. La "write_category_data_csv" fonction écrit les données de tous les livres d'une catégorie dans un fichier CSV. La "scrap_categories" fonction récupère toutes les URL de catégorie de la page principale.

Le script peut être exécuté pour récupérer les données de tous les livres sur le site Web ou pour une catégorie spécifique. Il crée un fichier CSV distinct pour chaque livre et un fichier CSV distinct pour chaque catégorie. Il télécharge et enregistre également les images de couverture du livre dans un répertoire séparé.

Avant de commencer, cloner le projet en local sur votre machine, copiez l'URL de ce repo et lancez la commande suivante:

git clone git@github.com:Ben10370/openclassroom_projet2.git (SSH)

git clone https://github.com/Ben10370/openclassroom_projet2.git (HTTPS)

Mise en place du projet :

Ce script à été créer avec python version 3.8.10

Créer et activer l'environnement virtuel, puis exécuter le code d'application.

--- Pour créer un environnement virtuel, dans la racine du projet, en votre terminal exécutez la commande python -m venv "nom de l'environnement"

--- Pour activer l'environnement, exécutez source env/bin/activate (si vous êtes sous Windows, la commande sera env/Scripts/activate.bat).

À ce stade, votre terminal ajoutera probablement le nom de votre environnement au début de chaque ligne de votre terminal. Si vous exécutez pip freeze, vous ne devriez maintenant pas voir de paquet répertorié. Cela montre qu'aucun paquet n'est installé dans votre environnement virtuel. C'est le comportement par défaut lorsque vous créez un environnement virtuel.

--- cd dans le répertoire où se trouve requirements.txt et dans votre terminal utilisez pip install -r requirements.txt

--- Dans la racine du projet, dans votre terminal tapez python (ou python3) main.py pour que la magie commence

--- Si vous deviez « quitter » ou « désactiver » votre environnement virtuel, exécutez la commande deactivate pendant que votre environnement virtuel est activé. Selon le terminal que vous utilisez, le suffixe (env) n’apparaîtra plus.
