#! env/bin/python3
""" File module to regroup all functions that concern the folders, the .csv and book's covers """

from requests import get
from pathlib import Path
import shutil
import csv


pathExtraction = Path("./extractions")
pathCovers = Path(f"{pathExtraction.resolve()}/couvertures")

# --
def addRows(fileName, informations):
    """ Add informations in the 'fileName.csv' (forbiden caracters will be remove).
        File is create with headers if it doesn't exist.

        Arguments :
            fileName (str) :        name of file without extension
            informations (dict) :   rows to add in file
    """
    addFolders()

    pathCSV = Path(f"{pathExtraction.resolve()}/{adaptFileName(fileName)}.csv")
    with open (pathCSV.resolve(), "a") as fichier:
        wtr = csv.DictWriter(fichier, fieldnames=informations[0].keys())
        wtr.writeheader()                                                   # Auto ignore if already add
        wtr.writerows(informations)


def copyCover(url, fileName):
    """ Download the file given by url in the folder './extractions/Couvertures'
        with the name 'fileName' (forbiden caracters will be remove).

        Arguments :
            url (str) :          Complete link
            fileName (str):      Name for the new file
    """

    addFolders()

    download = get(url)
    with open(f"{pathCovers.resolve()}/{adaptFileName(fileName)}.jpg", "wb") as image:
        image.write(download.content)

# --
def addFolders():
    """ Add the folders ./extractions and ./extractions/couvertures """

    try:
        if not pathExtraction.exists():
           pathExtraction.mkdir()
           pathCovers.mkdir()
    except:
        raise PermissionError

def removeFolders():
    """ Remove the folders (and their files) ./extractions and ./extractions/couvertures """

    try:
        if pathExtraction.exists():
            shutil.rmtree(pathExtraction.resolve())
    except:
        raise PermissionError

# --
def adaptFileName(txt):
    """ Return txt with only alphanum caracters """

    txt = "".join(["-" if c == "-" else " " if not c.isalnum() else c for c in txt])
    return " ".join(txt.split())

