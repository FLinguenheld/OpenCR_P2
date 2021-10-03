#! env/bin/python3
""" Module livre regroupant la gestion du dossier extraction et des fichiers csv & jpg """

from requests import get
from pathlib import Path
import shutil
import csv

import livre


pathExt = Path("./extractions")
pathImg = Path(f"{pathExt.resolve()}/Images")

# --
def ajouterLivre(nomFichier, informations):
    """ Ajoute la liste 'informations' dans le fichier csv renseigné.
        Le fichier est créé s'il n'existe pas, avec l'ajout des en-têtes (Constante livre.ENTETE).

        Arguments :
            nomFichier (str) :      Nom du fichier csv sans son extension
            informations (list) :   Informations à ajouter
    """

    ajouterDossiers()

    pathCSV = Path(f"{pathExt.resolve()}/{nomFichier}.csv")
    if not pathCSV.exists():
        with open (pathCSV.resolve(), "w") as fichier:
            wtr = csv.writer(fichier)
            wtr.writerow(livre.ENTETE)
    # --
    with open (pathCSV.resolve(), "a") as fichier:
        wtr = csv.writer(fichier)
        wtr.writerow(informations)


def copierCouverture(url, nomFichier):
    """ Télécharge le fichier renseigné dans le dossier ./extractions/Images

        Arguments :
            url (str) :          Lien complet
            nomFichier (str):    Nom du nouveau fichier
    """

    ajouterDossiers()

    # Adapte le nom du fichier
    nom = "".join(["-" if c == "-" else " " if not c.isalnum() else c for c in nomFichier])
    nom = " ".join(nom.split())

    telechargement = get(url)
    with open(f"{pathImg.resolve()}/{nom}.jpg", "wb") as image:
        image.write(telechargement.content)


def ajouterDossiers():
    """ Ajoute les dossiers ./extractions et ./extractions/Images. """

    try:
        if not pathExt.exists():
           pathExt.mkdir()
           pathImg.mkdir()
    except:
        raise PermissionError

def supprimerDossiers():
    """ Supprime les dossiers ./extractions et ./extractions/Images. """

    try:
        if pathExt.exists():
            shutil.rmtree(pathExt.resolve())
    except:
        raise PermissionError

