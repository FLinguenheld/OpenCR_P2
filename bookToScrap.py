#! env/bin/python3
""" Script create to scrap the website http://books.toscrape.com/
    It find all categories and all books to extract informations and write in a CSV files.
    Download covers of each books too """

from math import floor

from connect import urlToSoup
import files
from category import getBooksByCategory
from progressBar import showProgressBar


counterBooks = 0
counterCategory = 0

try:
    files.removeFolders()

    soup = urlToSoup("http://books.toscrape.com/")
    liste = soup.find("ul", class_="nav nav-list").find("ul").find_all("a")
    liste.sort(key=lambda elem : elem.string)                                       # Sort for better display

    print("Traitement en cours...")
    for i, c in enumerate(liste):
        progression = [13, floor(i * 13 / len(liste)), ""]                          # List [total, done, text] - 13 arbitrarily
        bookList = getBooksByCategory("http://books.toscrape.com/" + c["href"], progression)

        progression[2] = f"{bookList[0]} - Enregistrement csv"                      # Useless ?
        showProgressBar(progression)

        files.addRows(bookList[0], bookList[1])                                     # Save csv

        for l in bookList[1]:                                                       # Download cover
            progression[2] = f"{bookList[0]} - Copie couverture : {l['title'][:60]}"
            showProgressBar(progression)

            files.copyCover(l["image_url"], f"{l['title'][:60]} - {l['universal_product_code']}")
            counterBooks += 1

        counterCategory += 1
        
    print("\033[KTerminé.")


except AttributeError:
    print("\nErreur lors de la recherche d'une balise - Extraction impossible")     # HTML modified -> check the soup.find
except ConnectionError:
    print("\nEchec de la connexion au site")
except KeyboardInterrupt:
    print("\nArret par l'utilisateur")
except PermissionError:
    print("\nImpossible de supprimer/créer le dossier d'extraction")
finally:
    print(f"\033[K   - {counterCategory} catégorie(s) terminée(s)\n   - {counterBooks} livre(s) traité(s)")

