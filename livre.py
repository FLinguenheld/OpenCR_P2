#! env/bin/python3

from requests import get
from bs4 import BeautifulSoup

# -- Global
compteurArticle = 0

# -- Conversions Int/Float
toInt = lambda chaine : int("".join([nb for nb in chaine if nb.isdigit()]))
toFloat = lambda chaine : float("".join([nb for nb in chaine if (nb.isdigit() or nb == '.')]))

# --
def lire(url):


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

        return info

# --
if __name__ == "__main__":
    liste = lire("http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html")
    for elt in liste:
        print(f"   -  {elt}")

