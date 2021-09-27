#! env/bin/python3

from requests import get
from bs4 import BeautifulSoup

# -- Conversions Int/Float
toInt = lambda chaine : int("".join([nb for nb in chaine if nb.isdigit()]))
toFloat = lambda chaine : float("".join([nb for nb in chaine if (nb.isdigit() or nb == '.')]))

continuer = "O"
while continuer.upper() == "O":

    # Url ?
    #url = input("Entrer une adresse \n")
    #page = get(url)

    dico = {}


    page = get("http://books.toscrape.com/catalogue/libertarianism-for-beginners_982/index.html").content
    soup = BeautifulSoup(page, 'html.parser')


    # -- Catégorie
    categorie = soup.find("ul", class_="breadcrumb").find_all("a")
    if len(categorie) >= 3:
        dico["category"] = categorie[2].string

    # --
    dico["title"] = soup.find("div", class_="col-sm-6 product_main").find("h1").string

    # -- Review rating
    chiffres = ("One", "Two", "Three", "For", "Five")
    for i, elt in enumerate(chiffres):
        etoiles = soup.find("div", class_="col-sm-6 product_main").find("p", class_=f"star-rating {elt}")

        if etoiles != None:
            dico["review_rating"] = i + 1

    # --
    listeTD = soup.find("table", class_="table table-striped").find_all('td')
    dico["universal_product_code"] = toInt(listeTD[0].string)
    dico["price_including_tax"] = toFloat(listeTD[2].string)
    dico["price_excluding_tax"] = toFloat(listeTD[3].string)
    dico["number_available"] = toInt(listeTD[5].string)
    #dico["review_rating"] = listeTD[6].string

    # -- Description
    description = soup.find("article", class_="product_page").find_all("p")
    dico["product_description"] = description[3].string


    for t, c in dico.items():
        print(f" - {t}     -     {c}")

    continuer = input("Continuer ? O/N")

