#! env/bin/python3

from urllib.parse import urljoin

from requests import get
from bs4 import BeautifulSoup

import livre
import fichiers

# -- Global
compteurCategorie = 0

# --
def lecture(url, progression):

    global compteurCategorie
    page = get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        catEnCours = soup.find('div', class_='page-header action').find('h1').string


        while True:
            page = get(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")

                for elt in soup.find_all("h3"):
                    infoLivre = livre.lire(f"http://books.toscrape.com/catalogue/{elt.find('a')['href'][8:]}")

                    # -- Progression
                    afficherProgression(progression, f"{infoLivre[7]} -> {infoLivre[2][:60]}")
                    fichiers.ajouterLivre(infoLivre[7], infoLivre)
                    fichiers.copierCouverture(infoLivre[9], infoLivre[2], infoLivre[1])


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


# -- Affichage de la progression
compteur = 0
def afficherProgression(progression, txt):
    """ Fait évoluer la progression pour faire tourner la barre en cours ;)
    """
    global compteur
    l = ["|", "/", "–", "\\", "|", "/", "–", "\\"]

    compteur += 1
    if compteur >= 8:
        compteur = 0

    for i, c in enumerate(progression):
        if c == "–":
            #progression =  f"[{progression[:i]}{l[compteur]}{progression[i:]}]" 
            progression =  f"[{l[compteur]}]" 
            break

    print(f"\033[K{progression} -> {txt}", end="\r")        # \033[K : permet d'effacer la ligneo




# --
if __name__ == "__main__":
    lecture("http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html", "[–]")

