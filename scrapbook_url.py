import requests
from bs4 import BeautifulSoup

# Fonction qui récupère les url d'une catégory de livre

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
            book_url = article.find("a")["href"][8:] #récupérer url d'un livre
            book_url = f"https://books.toscrape.com/catalogue{book_url}"
            book_urls.append(book_url) #ajouter url du livre a la liste book_urls
            
        # integrer le bouton page suivante
        if soup.find("li", class_="next"): # Si le bouton page suivante existe
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
        

category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

urls = scrap_category(category_url)
print(urls, len(urls))
