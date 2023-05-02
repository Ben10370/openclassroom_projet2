import requests
from bs4 import BeautifulSoup
import csv
import os

def download_image(img_url, title, category):
    """
    Télécharge une image de livre et la stocke localement dans le dossier images_books/catégorie.

    Args:
        img_url (str): L'URL de l'image à télécharger.
        title (str): Le titre du livre.
        category (str): La catégorie du livre.

    Returns:
        None
    """
    category_dir = os.path.join("images_books", category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)
    filename = f"{title.replace(' ', '_').replace('#', '_').replace('/', '_').replace(':', '_')}.jpg"
    filepath = os.path.join(category_dir, filename)
    r = requests.get(img_url, stream=True)
    if r.ok:
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                

def scrap_book(book_url):
    """
    Récupère les données d'un livre à partir de son URL et les retourne sous forme de dictionnaire.

    Args:
        book_url (str): L'URL du livre à récupérer.

    Returns:
        dict: Un dictionnaire contenant les données du livre, y compris son titre, son URL, son UPC, son prix hors taxe,
            son prix TTC, sa disponibilité en stock, sa description de produit, sa catégorie, sa note de revue et son URL d'image.
    """
    r = requests.get(book_url)
    if r.ok:
        soup = BeautifulSoup(r.content, "html.parser")
    else:
        raise Exception("Bad request !")

    book_data = {}
    book_data["url"] = book_url
    book_data["title"] = soup.h1.text
    book_data["upc"] = soup.find_all("td")[0].text
    book_data["price_excl_tax"] = soup.find_all("td")[2].text
    book_data["price_incl_tax"] = soup.find_all("td")[3].text
    book_data["stock_available"] = soup.find_all("td")[5].text
    book_data["product_description"] = soup.find_all("p")[3].text
    book_data["category"] = soup.find_all("a")[3].text
    book_data["review_rating"] = soup.find_all("td")[6].text
    cover_url = soup.img["src"][5:]
    book_data["img_url"] = f"https://books.toscrape.com{cover_url}"
    
    download_image (book_data["img_url"], book_data["title"], book_data["category"])
    
    return book_data


def write_book_data_csv(book_data):
    """
    Écrit les données d'un livre dans un fichier CSV à partir d'un dictionnaire.

    Args:
        book_data (dict): Un dictionnaire contenant les données du livre, y compris son titre, son URL, son UPC, son prix hors taxe,
            son prix TTC, sa disponibilité en stock, sa description de produit, sa catégorie, sa note de revue et son URL d'image.

    Returns:
        None
    """
    with open(f'{book_data["title"]}.csv', mode="w") as f:
        writer = csv.writer(f)

        liste_cle = []
        for cle in book_data.keys():
            liste_cle.append(cle)
        print(liste_cle)
        writer.writerow(liste_cle)

        liste_valeur = []
        for valeur in book_data.values():
            liste_valeur.append(valeur)
        print(liste_valeur)
        writer.writerow(liste_valeur)
        

def scrap_category(url):
    """
    Récupère les URLs de tous les livres d'une catégorie et les renvoie sous forme d'une liste.

    Args:
        url (str): L'URL de la catégorie à scraper.

    Returns:
        list: Une liste contenant les URLs de tous les livres de la catégorie.
    """
    book_urls = []
    page_number = 2

    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.content, "html.parser")
    else:
        print()

    while True:
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            book_url = article.find("a")["href"][8:]
            book_url = f"https://books.toscrape.com/catalogue{book_url}"
            book_urls.append(book_url)

        if soup.find("li", class_="next"):
            next_page_url = url.replace("index.html", f"page-{page_number}.html")
            print(next_page_url)
            r = requests.get(next_page_url)
            if r.ok:
                soup = BeautifulSoup(r.content, "html.parser")
                page_number += 1
            else:
                print("la page n'existe pas :", next_page_url)
                break
        else:
            break

    return book_urls


def get_category_name_from_url(category_url):
    """
    Retourne le nom de la catégorie à partir de l'URL de la catégorie.
    
    Args:
        category_url: (str), URL de la catégorie
    Returns: 
        (str), nom de la catégorie
    """
    return category_url.split("/")[-2]


def write_category_data_csv(category_url):
    """
    Fonction qui récupère les données de tous les livres d'une catégorie et les écrit dans un fichier CSV.
    
    Args:
    - category_url (str): l'URL de la page de la catégorie dont on veut récupérer les données.
    
    Returns:
    - None
    
    Cette fonction utilise la fonction `scrap_category` pour récupérer les URL de tous les livres de la catégorie.
    Pour chaque livre, elle utilise la fonction `scrap_book` pour récupérer les données du livre.
    Elle stocke toutes les données dans un fichier CSV dans le dossier "csv_books_data" et utilise le nom de la catégorie
    pour nommer le fichier CSV.
    """
    book_urls = scrap_category(category_url)
    
    if not os.path.exists("csv_books_data"):
        os.makedirs("csv_books_data")
        
    csv_file_name = os.path.join("csv_books_data", f"{get_category_name_from_url(category_url)}.csv")

    with open(csv_file_name, mode="w") as f:
        writer = csv.writer(f)
        headers = [
            "url",
            "title",
            "upc",
            "price_excl_tax",
            "price_incl_tax",
            "stock_available",
            "product_description",
            "category",
            "review_rating",
            "img_url",
        ]
        writer.writerow(headers)

        for book_url in book_urls:
            book_data = scrap_book(book_url)
            writer.writerow(book_data.values())
            
category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
write_category_data_csv(category_url)


def scrap_categories():
    """
    Récupère les URL de toutes les catégories du site "https://books.toscrape.com/" sous forme de liste.

    Returns:
        category (list): Liste des URL de toutes les catégories du site "https://books.toscrape.com/".
    """
    url = "https://books.toscrape.com/index.html"
    category = []

    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.content, "html.parser")
    else:
        print("impossible d'afficher la page")

    nav = soup.find("ul", class_="nav nav-list")
    links = nav.find_all("a")
    for link in links:
        cat_url = link["href"][0:]
        cat_url = f"https://books.toscrape.com/{cat_url}"
        category.append(cat_url)

    return category


def write_all_categories_data():
    """
    Fonction qui écrit les données de tous les livres de toutes les catégories dans un fichier CSV.

    La fonction récupère toutes les URL des catégories en appelant la fonction 'scrap_categories', 
    puis pour chaque URL de catégorie, elle appelle la fonction 'write_category_data_csv' pour écrire 
    les données de tous les livres de cette catégorie dans un fichier CSV et les stocke dans un dossier 
    'csv_books_data' créé à cet effet.

        Aucun paramètre n'est requis.

    Returns:
        None.
    """
    categories = scrap_categories()[1:]
    for category_url in categories:
        write_category_data_csv(category_url)
        
write_all_categories_data()