#! env/bin/python3

from requests import get
from bs4 import BeautifulSoup

# -- Global
compteurArticle = 0

# -- Conversions Int/Float
toInt = lambda chaine : int("".join([nb for nb in chaine if nb.isdigit()]))
toFloat = lambda chaine : float("".join([nb for nb in chaine if (nb.isdigit() or nb == '.')]))
toNomImage = lambda chaine : "".join([" " if not c.isalnum() else c for c in chaine])           # Supp les ponctuations pour le nom du fichier image

# -- Affichage de la progression
compteur = 0
def etoile(txt):
    """ Fait évoluer la progression pour faire tourner la barre en cours ;)
    """
    global compteur
    l = ["|", "/", "–", "\\", "|", "/", "–", "\\"]

    compteur += 1
    if compteur >= 8:
        compteur = 0

    for i, c in enumerate(txt):
        if c == "–":
            return txt[:i-1] + l[compteur] + txt[i:]

    return txt

# --
def lectureArticle(url, cheminImage, progression):

    """ Fonction permettant de parser la page web d'un livre dans le site http://books.toscrape.com/
        chaque recherche est ajoutée dans une liste qui est retournée à la fin de cette fonction
        L'ordre des ajouts correspond à la liste des en-têtes définie dans le module "catégorie"

        Télécharge également la couverture du livre dans le dossier ./Images (le dossier doit exister)

        Affiche la progression avec le texte renseigné en argument plus la catégorie et le début du nom du livre.

        Arguments :
            url (str) :         url de l'article à parser
            cheminImage (str) : chemin du dossier où télécharger les images (le dossier doit exister)
            progression (str) : texte de progression à afficher dans le terminal (à gauche des ajouts de cette fonction)
    """

    global compteurArticle
    info = list()
    page = get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        # -- 0 - product_page_url
        info.append(url)

        # --
        listeTD = soup.find("table", class_="table table-striped").find_all('td')
        info.append(listeTD[0].string)                                              # -- 1 - universal_product_code

        # -- 2 - title
        info.append(soup.find("div", class_="col-sm-6 product_main").find("h1").string)

        # -- Progression
        print(f"\033[K{etoile(f'{progression} -> {info[2][:60]}')}", end="\r")        # \033[K : permet d'effacer la ligne

        # --
        info.append(toFloat(listeTD[2].string))                                     # -- 3 - price_including_tax
        info.append(toFloat(listeTD[3].string))                                     # -- 4 - price_excluding_tax
        info.append(toInt(listeTD[5].string))                                       # -- 5 - number_available

        # -- 6 - product_description
        info.append(soup.find("article", class_="product_page").find_all("p")[3].string)

        # -- 7 - category
        info.append(soup.find("ul", class_="breadcrumb").find_all("a")[2].string)

        # -- 8 - review_rating
        chiffres = ("One", "Two", "Three", "Four", "Five")
        for i, elt in enumerate(chiffres):
            etoiles = soup.find("div", class_="col-sm-6 product_main").find("p", class_=f"star-rating {elt}")

            if etoiles != None:
                info.append(i + 1)
                break

        # -- 9 - image_url
        info.append("http://books.toscrape.com" + soup.find("img", alt=info[2])["src"][5:])   # Utilise le title pour la recherche

        # -- Téléchargement de l'image
        telechargement = get(info[9])
        with open(f"{cheminImage}/{toNomImage(info[2])[:60]} - {info[1]}.jpg", "wb") as image:
            image.write(telechargement.content)

        # -- Progression
        print(f"\033[K{etoile(f'{progression} -> {info[2][:60]}')}", end="\r")        # \033[K : permet d'effacer la ligne
        compteurArticle += 1

        return info

# --
if __name__ == "__main__":
    liste = lectureArticle("http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",  "./extractions", "Test : ")
    for elt in liste:
        print(f"   -  {elt}")

