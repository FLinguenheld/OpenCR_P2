#! env/bin/python3
""" File module to regroup all functions that concern the folders, the .csv and book's covers """

from requests import get
from pathlib import Path
import shutil
import csv


pathExtraction = Path("./extractions")
pathCovers = Path(f"{pathExtraction.resolve()}/Couvertures")

# --
def addRows(fileName, informations, headers):
    """ Add list informations in the 'fileName.csv'.
        File is create with headers if it doesn't exist.

        Arguments :
            fileName (str) :        name of file without extension
            informations (list) :   rows to add in file
    """

    addFolders()

    pathCSV = Path(f"{pathExtraction.resolve()}/{fileName}.csv")
    if not pathCSV.exists():
        with open (pathCSV.resolve(), "w") as fichier:
            wtr = csv.writer(fichier)
            wtr.writerow(headers)
    # --
    with open (pathCSV.resolve(), "a") as fichier:
        wtr = csv.writer(fichier)
        wtr.writerows(informations)


def copyCover(url, fileName):
    """ Download the file given by url in the folder './extractions/Couvertures'
        with the name 'fileName' (forbiden caracters will be remove).

        Arguments :
            url (str) :          Complete link
            fileName (str):      Name for the new file
    """

    addFolders()

    # Check and adapt the fileName
    name = "".join(["-" if c == "-" else " " if not c.isalnum() else c for c in fileName])
    name = " ".join(name.split())

    download = get(url)
    with open(f"{pathCovers.resolve()}/{name}.jpg", "wb") as image:
        image.write(download.content)


def addFolders():
    """ Add the folders ./extractions and ./extractions/Couvertures """

    try:
        if not pathExtraction.exists():
           pathExtraction.mkdir()
           pathCovers.mkdir()
    except:
        raise PermissionError

def removeFolders():
    """ Remove the folders (and their files) ./extractions and ./extractions/Couvertures """

    try:
        if pathExtraction.exists():
            shutil.rmtree(pathExtraction.resolve())
    except:
        raise PermissionError

