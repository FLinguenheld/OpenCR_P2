#! env/bin/python3

from categorie import lectureCategorie
from pathlib import Path
import shutil
from requests import get
from bs4 import BeautifulSoup


path = Path("./extractions")

page = get("http://books.toscrape.com/")
if page.status_code == 200:

    # Suppression du dossier de sortie
    try:
        if path.exists():
            shutil.rmtree(path.resolve())
    except:
        print(f"Impossible de supprimer le dossier {path.resolve()}")     # Arrêt --
    else:

        # Création du dossier et récup des catégories
        path.mkdir()

        soup = BeautifulSoup(page.content, "html.parser")
        liste = soup.find("ul", class_="nav nav-list").find("ul").find_all("a")

        for c in liste:
            lectureCategorie("http://books.toscrape.com/" + c["href"], path.resolve())
