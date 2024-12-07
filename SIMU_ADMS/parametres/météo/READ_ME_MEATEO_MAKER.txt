Guide pour utiliser code meteo_maker_1.py

-> Ce code est un générateur de fichier .met à partir des fichiers .csv dispo en open-source sur meteo.data.gouv.fr

-> Renomer fichier source .csv dans le code pour le faire correspondre au nom du fichier
-> mettre .csv et .py dans le meme dossier (chemin non indiqué dans script)
-> Ouvrir le fichier .csv 
-> Retirer colonnes vides et non utiles (variable non désirée)
-> Retirer lignes non utiles (périodes ou lieux non désirés)
-> Lancer exécution
-> Vérifier résultat dans le fichier donnees.txt (potentiel bug a corriger à la main dans les noms de variable en haut de ficher)

-> Si variables en plus désirées, se referer aux lignes 135 à 137 ou certaines sont supprimées en plus de celles initialement supprimé sur le .csv
