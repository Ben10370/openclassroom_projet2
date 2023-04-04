import requests
from bs4 import BeautifulSoup
import csv

# Fonction qui récupère les url d'une catégory de livre


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

    return book_data


def write_book_data_csv(book_data):
    
    # Ecrire un fichier csv contenant les données du livre à partir d'un dictionnaire.

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
    
    # Renvoie les URL des livres sous forme de liste.
    
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


def get_category_name_from_url(category_url):
    
    # Renvoie le nom de la catégorie à partir de l'URL de la catégorie.
   
    return category_url.split("/")[-2]


def write_category_data_csv(category_url):
    
    # Ecrire un fichier csv contenant toutes les données du livre d'une catégorie.
    
    book_urls = scrap_category(category_url)

    with open(f"{get_category_name_from_url(category_url)}.csv", mode="w") as f:
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


category_url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
write_category_data_csv(category_url)


def scrap_categories():
    
    # Renvoie une liste d'URL de catégorie

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