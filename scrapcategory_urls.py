import requests
from bs4 import BeautifulSoup

# Fonction qui récupére les urls de toute les category de livres sur la page d'acceuil.

def scrap_categories():
    
    url = "https://books.toscrape.com/index.html"
    category = []
    
    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.content, "html.parser")
    else:
        print("impossible d'afficher la page")
    
    nav = soup.find("ul", class_= "nav nav-list")
    links = nav.find_all("a")
    for link in links:
        cat_url = link["href"][0:]
        cat_url = f"https://books.toscrape.com/{cat_url}"
        category.append(cat_url)
    
    return category
    
print(scrap_categories())
   
