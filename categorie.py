#! env/bin/python3

from article import lectureArticle
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


def lectureCategorie(url, cheminDossier):

    page = get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        catEnCours = soup.find('div', class_='page-header action').find('h1').string
        print(f" -- Catégorie en cours : {catEnCours}")

        enTete = ["product_page_url",
                "universal_product_code",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url"]

        with open(f"{cheminDossier}/{catEnCours}.csv", "w") as fichier:
            writer = csv.writer(fichier)
            writer.writerow(enTete)

            i = 1
            while True:

                page = get(url)
                print(f" -- Page {i}")
                if page.status_code == 200:
                    soup = BeautifulSoup(page.content, "html.parser")

                    for elt in soup.find_all("h3"):
                       writer.writerow(lectureArticle("http://books.toscrape.com/catalogue" + elt.find("a")["href"][8:]))

                    suiv = soup.find("li", class_="next")
                    if suiv != None:
                        url = urljoin(page.url, suiv.find("a")["href"])
                        i += 1
                    else:
                        print(" -- Fin")
                        break

                else:
                    print(f"Impossible d'acceder à {url}")
                    break


# --
if __name__ == "__main__":
   lectureCategorie("http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html", "./extractions")
