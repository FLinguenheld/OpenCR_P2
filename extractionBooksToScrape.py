#! env/bin/python3

from categorie import lectureCategorie
from pathlib import Path
import shutil
from requests import get
from bs4 import BeautifulSoup


path = Path("./extractions")
pathImg = Path(f"{path.resolve()}/Images")

page = get("http://books.toscrape.com/")
if page.status_code == 200:

    # Suppression du dossier de sortie
    try:
        if path.exists():
            shutil.rmtree(path.resolve())
    except:
        print(f"Impossible de supprimer le dossier {path.resolve()}")     # Arrêt --
    else:
        path.mkdir()        # Création des dossiers
        pathImg.mkdir()

        # -- Recherche des catégories et lancement des lectures
        soup = BeautifulSoup(page.content, "html.parser")
        liste = soup.find("ul", class_="nav nav-list").find("ul").find_all("a")
        print("Traitement en cours")

        # -- Création d'une barre de progression envoyée au module article pour l'affichage
        progression = str()
        for i, c in enumerate(liste):
            progression = "["
            for j in range(15):
                if j <= int(i * 15 / len(liste)):
                    progression +="X"
                else:
                    progression +="–"

            progression += "]"

            # --
            lectureCategorie("http://books.toscrape.com/" + c["href"], path.resolve(), progression)

        print("Extraction terminée")
