## OpenCR_P2
OpenClassRooms Projet 2  
Utilisez les bases de Python pour l'analyse de marché  
2021-09-29

![Logo FLinguenheld](https://github.com/FLinguenheld/OpenCR_P2/blob/main/Forelif.png "Pouet")

### Environnement virtuel
La liste des paquets nécessaires est enregistrée dans le fichier requirements.txt  
Pour les installer, utilisez la commande :  
>pip install -r requirements.txt


Activez l'environnement virtuel avec la commande :  
>source env/bin/activate

### Programme
Autorisez l'execution du fichier extractionBooksToScrape.py :  
>chmod +x extractionBooksToScrape.py


lancez le script :  
>./extractionBooksToScrape.py

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
