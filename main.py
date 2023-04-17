import requests
from bs4 import BeautifulSoup
import csv
import os

# Fonction qui télécharge les images des livres et les stock en local dans le dossier du programme, puis sous dossier images_books puis sous dossiers de chaques catégories.

def download_image(img_url, title, category):
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
                
# Fonction qui récupère les données d'un livre sous forme de dictionnaire.

def scrap_book(book_url):
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

# Fonction qui écrit les données d'un livre dans un fichier CSV à partir d'un dictionnaire.

def write_book_data_csv(book_data):
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

# Fonction qui récupère les URL de tous les livres d'une catégorie et les renvoies sous forme d'une liste.

def scrap_category(url):
    
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
            book_url = article.find("a")["href"][8:]  # récupérer url d'un livre
            book_url = f"https://books.toscrape.com/catalogue{book_url}"
            book_urls.append(book_url)  # ajouter url du livre a la liste book_urls

        # integrer le bouton page suivante
        if soup.find("li", class_="next"):  # Si le bouton page suivante existe
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

# Fonction qui retourne le nom de la catégorie à partir de l'URL de la catégorie.

def get_category_name_from_url(category_url):
    
    return category_url.split("/")[-2]

# Fonction qui écrit les données de tous les livres d'une catégorie dans un fichier CSV et les stocks dans un dossier csv_books_data.

def write_category_data_csv(category_url):
    
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

# Fonction qui récupère les URL de toutes les catégories sous forme de liste.

def scrap_categories():

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

# Fonction qui écrit les données de tous les livres de toutes les catégories dans un fichier CSV.

def write_all_categories_data():
    categories = scrap_categories()[1:]
    for category_url in categories:
        write_category_data_csv(category_url)
        
write_all_categories_data()