#! env/bin/python3
""" Book module to scrap a book in the website http://books.toscrape.com/ """

from requests import get
from bs4 import BeautifulSoup

from progressBar import showProgressBar


HEADER = [      "product_page_url",
                "universal_product_code",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url"]


# -- Conversions Int/Float
toInt = lambda chaine : int("".join([nb for nb in chaine if nb.isdigit()]))
toFloat = lambda chaine : float("".join([nb for nb in chaine if (nb.isdigit() or nb == '.')]))

# --
def getBook(url, progression = [0, 0, ""]):
    """ Scan the page given by url to fill and return a list with informations.
        The order of informations is given by the constant HEADER.

        Arguments :
            url (str) :            Complete link to book's page of BookToScrap
            progression (list) :   (total, done, text) display a progress bar (total = 0 to hide)
    """

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
        if progression[0] > 0:
            progression[2] += info[2][:60]
            showProgressBar(progression)

        # --
        info.append(toFloat(listeTD[2].string))                                     # -- 3 - price_including_tax
        info.append(toFloat(listeTD[3].string))                                     # -- 4 - price_excluding_tax
        info.append(toInt(listeTD[5].string))                                       # -- 5 - number_available

        # -- 6 - product_description
        info.append(soup.find("article", class_="product_page").find_all("p")[3].string)

        # -- 7 - category
        info.append(soup.find("ul", class_="breadcrumb").find_all("a")[2].string)

        # -- 8 - review_rating
        number = ("One", "Two", "Three", "Four", "Five")
        for i, elt in enumerate(number):
            stars = soup.find("div", class_="col-sm-6 product_main").find("p", class_=f"star-rating {elt}")

            if stars is not None:
                info.append(i + 1)
                break

        # -- 9 - image_url
        info.append("http://books.toscrape.com" + soup.find("img", alt=info[2])["src"][5:])   # Use the title to search

        # --
        return info

    else:
        raise ConnectionError


# --
if __name__ == "__main__":
    infoList = getBook("http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html")
    print("Lecture du livre Tipping the velvet 999 :")
    for elt in infoList:
        print(f"   -  {elt}")

