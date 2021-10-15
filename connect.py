#! env/bin/python3

from requests import get
from bs4 import BeautifulSoup


def urlToSoup(url):
    """ Simplify the connection to url and return a soup (html parser)
        Return a soup or raise a ConnectionError

        Arguments :
            url (str) :     Complete link to webpage
    """

    try:
        page = get(url)
        if page.status_code == 200:
            return BeautifulSoup(page.content, "html.parser")                               # Url for each category
        else:
            raise ConnectionError
    except :
        raise ConnectionError


if __name__ == "__main__":
    soup = urlToSoup("http://books.toscrape.com/")

