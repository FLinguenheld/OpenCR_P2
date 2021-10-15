#! env/bin/python3
""" Book module to scrap a book in the website http://books.toscrape.com/ """

from connect import urlToSoup
from progressBar import showProgressBar


# -- Conversions Int/Float
toInt = lambda chaine : int("".join([nb for nb in chaine if nb.isdigit()]))
toFloat = lambda chaine : float("".join([nb for nb in chaine if (nb.isdigit() or nb == '.')]))

# --
def getBook(url, progression = [0, 0, ""]):
    """ Scan the page given by url to fill and return a dictionary with informations.

        Arguments :
            url (str) :            Complete link to book's page of BookToScrap
            progression (list) :   (total, done, text) display a progress bar (total = 0 to hide)
    """

    soup = urlToSoup(url)
    info = dict()
    listeTD = soup.find("table", class_="table table-striped").find_all('td')

    info["product_page_url"] = url
    info["universal_product_code"] = listeTD[0].string
    info["title"] = soup.find("div", class_="col-sm-6 product_main").find("h1").string

    # --
    if progression[0] > 0:
        progression[2] += info["title"][:60]
        showProgressBar(progression)

    # --
    number = ("One", "Two", "Three", "Four", "Five")
    for i, elt in enumerate(number):
        stars = soup.find("div", class_="col-sm-6 product_main").find("p", class_=f"star-rating {elt}")

        if stars is not None:
            info["review_rating"] = i + 1
            break

    # --
    info["category"] = soup.find("ul", class_="breadcrumb").find_all("a")[2].string
    info["price_including_tax"] = toFloat(listeTD[2].string)
    info["price_excluding_tax"] = toFloat(listeTD[3].string)
    info["number_available"] = toInt(listeTD[5].string)
    info["product_description"] = soup.find("article", class_="product_page").find_all("p")[3].string
    info["image_url"] = "http://books.toscrape.com" + soup.find("img", alt=info["title"])["src"][5:]   # Use the title to search

    # --
    return info


# --
if __name__ == "__main__":
    infos = getBook("http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html")
    print("Lecture du livre Tipping the velvet 999 :")
    for c, val in infos.items():
        print(f"   - {c}   -> {val}")

