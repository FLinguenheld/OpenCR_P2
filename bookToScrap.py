#! env/bin/python3
""" Programme permettant de parcourir l'ensemble du site http://books.toscrape.com/ afin
    d'extraire et d'enregistrer des informations pour chaque livre """

from requests import get
from bs4 import BeautifulSoup
from math import ceil

import livre
import categorie
import fichiers


page = get("http://books.toscrape.com/")
if page.status_code == 200:

    try:
        fichiers.supprimerDossiers()

        soup = BeautifulSoup(page.content, "html.parser")                               # Liens de toutes les catégories
        liste = soup.find("ul", class_="nav nav-list").find("ul").find_all("a")
        liste.sort(key=lambda elem : elem.string)                                       # Affichage plus agréable

        print("Traitement en cours...")
        for i, c in enumerate(liste):
            progression = ceil(i * 13 / len(liste)), 13                                  # Tuple : (Fait, Total)
            categorie.lecture("http://books.toscrape.com/" + c["href"], progression)

    except AttributeError:
        print("\nErreur lors de la recherche d'une balise - Extraction impossible")     # Site modifié, revoir les soup.find
    except ConnectionError:
        print("\nEchec de la connexion au site")
    except KeyboardInterrupt:
        print("\nArret par l'utilisateur")
    except PermissionError:
        print("\nImpossible de supprimer/créer le dossier d'extraction")
    finally:
        print(f"\n{livre.compteurLivre} livres traité(s) dans {categorie.compteurCategorie} catégorie(s)")

