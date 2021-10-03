#! env/bin/python3

from pathlib import Path
import shutil
from requests import get
import csv


pathExt = Path("./extractions")
pathImg = Path(f"{pathExt.resolve()}/Images")

toNomImage = lambda chaine : "".join([" " if not c.isalnum() else c for c in chaine])           # Supp les ponctuations pour le nom du fichier image


def ajouterDossiers():
    if not pathExt.exists():
       pathExt.mkdir() 
       pathImg.mkdir()


def supprimerDossiers():
    try:
        if pathExt.exists():
            shutil.rmtree(pathExt.resolve())
    except:
        print(f"Impossible de supprimer le dossier {pathExt.resolve()}")     # Arrêt --


def ajouterLivre(categorie, informations):

    ajouterDossiers()

    pathCSV = Path(f"{pathExt.resolve()}/{categorie}.csv")
    if not pathCSV.exists():
        with open (pathCSV.resolve(), "w") as fichier:

            enTete = ["product_page_url",
                "universal_product_code",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url"]

            wtr = csv.writer(fichier)
            wtr.writerow(enTete)
    # --
    with open (pathCSV.resolve(), "a") as fichier:
        
        wtr = csv.writer(fichier)
        wtr.writerow(informations)


def copierCouverture(url, nomFichier, codeUPC):

    ajouterDossiers()

    telechargement = get(url)
    with open(f"{pathImg.resolve()}/{toNomImage(nomFichier)} - {codeUPC}.jpg", "wb") as image:
        image.write(telechargement.content)

