#! env/bin/python3
""" Module create to scrap all books of a category for BookToScrap.com """

from urllib.parse import urljoin

from requests import get
from bs4 import BeautifulSoup

from book import getBook


# --
def getBooksByCategory(url, progression = [0, 0, ""]):
    """ Scan the web page given by url, scrap the book's list to process one by one.
        Go to the next page if necessary.
        Return the category's name and a list with all book's informations.

        Arguments :
            url (str) :             Complete link to a category's page of BookToScrap
            progression (list) :    (total, done, text) display a progress bar (total = 0 to hide)
    """

    bookList = []
    numberPage = 1
    while True:
        page = get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")

            # Get the category name
            cat = soup.find('h1').string

            for elt in soup.find_all("h3"):
                progression[2] = f"{cat} - Page {numberPage} - "        # Only change the progress text
                bookList.append(getBook(f"http://books.toscrape.com/catalogue/{elt.find('a')['href'][8:]}", progression))

            # Next page ?
            nextPage = soup.find("li", class_="next")
            if nextPage is not None:
                url = urljoin(page.url, nextPage.find("a")["href"])
                numberPage += 1
            else:
                return cat, bookList

        else:
            raise ConnectionError
            break


# --
if __name__ == "__main__":
    print("Essai - Récupération de la catégorie 'add a comment'")
    liste = getBooksByCategory("http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html", [1, 0, ""])
    for l in liste[1]:
        print(f" - {l[2]}")
