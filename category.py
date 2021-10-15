#! env/bin/python3
""" Module create to scrap all books of a category for BookToScrap.com """

from urllib.parse import urljoin

from connect import urlToSoup
from book import getBook


# --
def getBooksByCategory(url, progression = [0, 0, ""]):
    """ Scan the web page given by url, scrap the book's list to process one by one (sort by title)
        Go to the next page if necessary.
        Return the category's name and a list with all book's informations.

        Arguments :
            url (str) :             Complete link to a category's page of BookToScrap
            progression (list) :    (total, done, text) display a progress bar (total = 0 to hide)
    """

    bookList = []
    numberPage = 1
    while True:
        soup = urlToSoup(url)

        # Get the category name
        cat = soup.find('h1').string

        # Get and sort the book list for better display
        l = soup.find_all("h3")
        l.sort(key=lambda elem : elem.find('a')['title'])

        for elt in l:
            progression[2] = f"{cat} - Page {numberPage} - "        # Only change the progress text
            bookList.append(getBook(f"http://books.toscrape.com/catalogue{elt.find('a')['href'][8:]}", progression))

        # Next page ?
        nextPage = soup.find("li", class_="next")
        if nextPage is not None:
            url = urljoin(url, nextPage.find("a")["href"])
            numberPage += 1
        else:
            return cat, bookList


# --
if __name__ == "__main__":
    print("Essai - Récupération de la catégorie 'add a comment'")
    retour = getBooksByCategory("http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html", [1, 0, ""])
    for elem in retour[1]:
        print(elem["title"])

