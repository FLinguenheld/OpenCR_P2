#! env/bin/python3
""" Module categorie regroupant la lecture d'une catégorie et l'affichage de la progression """

from urllib.parse import urljoin

from requests import get
from bs4 import BeautifulSoup

import livre
import fichiers


compteurCategorie = 0

# --
def lecture(url, progression):
    """ Récupère la liste des livres dans la page renseignée pour les traiter un par un.
        Enregistre les infos dans un fichier csv et télécharge la couverture.
        Passe à la page suivante si elle existe.

        Arguments :
            url (str) :             Lien complet de la catégorie à traiter
            progression (tuple) :   (fait, total) deux int permettant d'afficher la progression dans le terminal
    """

    global compteurCategorie

    while True:
        page = get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")

            for elt in soup.find_all("h3"):
                infoLivre = livre.lire(f"http://books.toscrape.com/catalogue/{elt.find('a')['href'][8:]}")

                afficherProgression(progression, f"{infoLivre[7]} -> {infoLivre[2][:60]}")          # Affiche la cat et livre en cours
                fichiers.ajouterLivre(infoLivre[7], infoLivre, livre.ENTETE)
                fichiers.copierCouverture(infoLivre[9], f"{infoLivre[2][:60]} - {infoLivre[1]}")

            # Page suivante ?
            suiv = soup.find("li", class_="next")
            if suiv is not None:
                url = urljoin(page.url, suiv.find("a")["href"])
            else:
                compteurCategorie += 1
                break

        else:
            raise ConnectionError
            break


# --
compteur = 0
def afficherProgression(progression, txt):
    """ Fait évoluer la progression pour faire tourner la barre en cours ;)

        Arguments :
            progression (tuple) :   (fait, total) int
            txt (str) :             Texte à afficher après la barre de progression
    """

    global compteur
    l = ["|", "/", "–", "\\", "|", "/", "–", "\\"]

    compteur += 1
    if compteur >= 8:
        compteur = 0

    p = str()
    for i in range(progression[0]):
        p += "X"

    p += l[compteur]

    for i in range(progression[1] - progression[0]):
        p += "–"

    print(f"\033[K[{p}] -- {txt}", end="\r")        # \033[K : permet d'effacer la ligneo


# --
if __name__ == "__main__":
    lecture("http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html", (0, 1))

