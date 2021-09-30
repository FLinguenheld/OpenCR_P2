#! env/bin/python3

from urllib.parse import urljoin
import csv

from requests import get
from bs4 import BeautifulSoup

import article

# -- Global
compteurCategorie = 0

# --
def lectureCategorie(url, cheminDossier, progression):

    """ Fonction permettant de lire et d'enregistrer dans un fichier csv des informations pour toute une catégorie
        d'article du site http://books.toscrape.com/
        Ces informations sont définies ici avec la liste "enTete" puis recueillies et retournées par le module "article"

        Étapes :
                    Création du fichier csv avec le nom de la catégorie (écrasé si existant)
                    Ajout des en-têtes
                    Traitement puis ajout de chaque article dans le fichier csv

        Arguments :
            url (str) :             url de la catégorie (sans la première partie : "http://books.toscrape.com/catalogue")
            cheminDossier (str) :   chemin du dossier où enregitrer le fichier csv (sans le / final)
            progression (str) :     texte de progression à afficher dans le terminal (complété ici puis affiché par le module "article")
    """

    global compteurCategorie
    page = get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        catEnCours = soup.find('div', class_='page-header action').find('h1').string

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

            while True:
                page = get(url)
                if page.status_code == 200:
                    soup = BeautifulSoup(page.content, "html.parser")

                    for elt in soup.find_all("h3"):
                        writer.writerow(article.lectureArticle("http://books.toscrape.com/catalogue" + elt.find("a")["href"][8:], f"{cheminDossier}/Images", f"{progression} -- {catEnCours}"))

                    compteurCategorie += 1

                    # Page suivante ?
                    suiv = soup.find("li", class_="next")
                    if suiv != None:
                        url = urljoin(page.url, suiv.find("a")["href"])
                    else:
                        break

                else:
                    print(f"Impossible d'acceder à {url}")
                    break


# --
if __name__ == "__main__":
    lectureCategorie("http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html", "./extractions", "Test : ")

