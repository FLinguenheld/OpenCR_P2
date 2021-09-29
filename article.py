#! env/bin/python3

from requests import get
from bs4 import BeautifulSoup

# -- Conversions Int/Float
toInt = lambda chaine : int("".join([nb for nb in chaine if nb.isdigit()]))
toFloat = lambda chaine : float("".join([nb for nb in chaine if (nb.isdigit() or nb == '.')]))

# -- Affichage de la progression
compteur = 0
def etoile(txt):
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
def lectureArticle(url, progression):

    info = list()
    page = get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        # -- product_page_url
        info.append(url)

        # --
        listeTD = soup.find("table", class_="table table-striped").find_all('td')
        info.append(toInt(listeTD[0].string))                                       # -- universal_product_code

        # -- title
        info.append(soup.find("div", class_="col-sm-6 product_main").find("h1").string)

        # -- Progression
        print(f"\033[K{etoile(f'{progression} -> {info[2][:60]}')}", end="\r")        # \033[K : permet d'effacer la ligne

        # --
        info.append(toFloat(listeTD[2].string))                                     # -- price_including_tax
        info.append(toFloat(listeTD[3].string))                                     # -- price_excluding_tax
        info.append(toInt(listeTD[5].string))                                       # -- number_available

        # -- product_description
        info.append(soup.find("article", class_="product_page").find_all("p")[3].string)

        # -- category
        info.append(soup.find("ul", class_="breadcrumb").find_all("a")[2].string)

        # -- review_rating
        chiffres = ("One", "Two", "Three", "Four", "Five")
        for i, elt in enumerate(chiffres):
            etoiles = soup.find("div", class_="col-sm-6 product_main").find("p", class_=f"star-rating {elt}")

            if etoiles != None:
                info.append(i + 1)
                break

        # -- image_url
        info.append("http://books.toscrape.com" + soup.find("img", alt=info[2])["src"][5:])   # Utilise le title pour la recherche

        return info


# --
if __name__ == "__main__":
    liste = lectureArticle("http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html", "Test : ")
    for elt in liste:
        print(f"   -  {elt}")


#lecturePage("http://books.toscrape.com/catalogue/our-band-could-be-your-life-scenes-from-the-american-indie-underground-1981-1991_985/index.html")
