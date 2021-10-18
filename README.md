## OpenCR_P2
OpenClassRooms Projet 2 
Utilisez les bases de Python pour l'analyse de marché 

![Logo FLinguenheld](https://github.com/FLinguenheld/OpenCR_P2/blob/main/Forelif.png "Pouet")
****
### Installation
Rendez vous dans le dossier de votre choix puis lancez un terminal. 
Clonez le dossier depuis GitHub avec la commande : 
>git clone https://github.com/FLinguenheld/OpenCR_P2 

Installez l'environnement virtuel :
>python3 -m venv env

Activez le :
>source env/bin/activate

Installez les paquets nécessaires à l'aide du fichier requirements.txt :
>pip install -r requirements.txt

Lancez le programme :
>./bookToScrap.py
****
### Déroulement
Le programme se connecte à <http://books.toscrape.com/>, parcourt les catégories puis chaque article 
Il y extrait les informations :
+ product_page_url
+ universal_product_code (upc)
+ title
+ price_including_tax
+ price_excluding_tax
+ number_available
+ product_description
+ category
+ review_rating
+ image_url


Puis les enregistre dans un fichier csv 
Un fichier csv par catégorie contenant tous les articles 


Il télécharge également la couverture de chaque article avec comme nom : 
titre du livre - UPC .jpg


Ces fichiers seront rangés dans le dossier extractions/ 
(Le dossier est supprimé à chaque lancement du programme) 


La progression est affichée avec la catégorie et le titre en cours 
L'execution dure plusieurs minutes (Control-C pour arrêter) 
