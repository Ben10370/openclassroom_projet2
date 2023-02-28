import requests
from bs4 import BeautifulSoup
import csv

book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
url = requests.get(book_url)
soup = BeautifulSoup(url.content, "html.parser")

# Fonction qui récupère les informations d'un livre

def scrap_book(book_url):

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

print(scrap_book(book_url))