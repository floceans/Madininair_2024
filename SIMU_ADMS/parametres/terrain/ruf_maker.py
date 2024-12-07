"""
@description: Créé fichier .ruf à partir d'un fichier .png et .ter couvrant même zone géographique
@author: Florent Puy
@date: 5 août 2024
"""


import numpy as np
import matplotlib.pyplot as plt
import PIL as pil
from fun_rug import *
from tqdm import tqdm
from colorama import Fore, Back, Style, init
import math

init()

## récupérer données ##
file_path_alti = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\terrain\CODE_PROPRE\concat\francois_sud\Francois_fregate_wsg_3395.ter'
file_path_ruf = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\terrain\CODE_PROPRE\concat\francois_sud\freg.png'

out_file_ruf = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\terrain\CODE_PROPRE\concat\francois_sud\fregate_oui.ruf'

print("\n")

coord_alti = read_file(file_path_alti)


# generer matrice coordonnées GPS
coord = parse_coordinates(file_path_alti)

nbr_col = len(coord_alti[0])
nbr_lin = len(coord_alti)


n_lati = 0
n_longi = 0
lati_1 = coord_alti[0][1]
longi_1 = coord_alti[0][2]

## Calcul taille de la matrice ##
## PAS FORCEMENT CARREE ##
for triplet in coord_alti:
    if triplet[2] != lati_1:
        n_lati += 1
        lati_1 = triplet[2]
        
n_longi = int(nbr_lin / n_lati)

print("nbr_longi : ", n_longi)
print("nbr_lati : ", n_lati)


redimensionner_image(file_path_ruf, n_lati, n_longi, "image_rugo_resized.png")
# Lire les données et les stocker dans une liste de listes #
ruf = pil.Image.open("image_rugo_resized.png")

#png to list of list
ruf = np.array(ruf)
ruf = ruf.tolist()

rugo = smooth_matrix(rugo_maker(ruf), 5)

print("\n")

print("Nombre de lignes alti: ", nbr_lin)
print("Nombre de colonnes alti: ", nbr_col)

print("\n")

print("Lignes rugo : ", len(rugo))
print("Colonnes rugo : ", len(rugo[0]))

print("\n")


rugo = matrice_en_liste(rugo)

print("Lignes rugo en liste : ", len(rugo))


with open(out_file_ruf, 'w') as f:
    # Parcourir la matrice et écrire chaque élément dans le fichier
    num_line = 0

    for triplet in tqdm(coord_alti, desc=f"{Fore.MAGENTA}Création du fichier{Style.RESET_ALL}",
                  bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.MAGENTA, Style.RESET_ALL)):
        
        x = triplet[1]
        y = triplet[2]
        
        value = rugo[num_line]

        if abs(value) < 0.0001:
            value = 0.0001

        num_line += 1
        
        f.write(f"{num_line},{x},{y},{value:.2E}\n")
        

            
            
print("\n")

print("Fichier ", out_file_ruf, " créé avec succès.")

print("Taille de la matrice : ", int(num_line))

if num_line > 770000 :
    print("Fichier trop volumineux pour être traité par ADMS : ", num_line, ". Réduire taille sous 770 000 valeurs.")



#rugo = liste_en_matrice(rugo)
x=[]
y=[]

for triplet in tqdm(coord_alti, desc=f"{Fore.MAGENTA}Création du graphique{Style.RESET_ALL}",
                  bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.MAGENTA, Style.RESET_ALL)):
    x.append(triplet[1])
    y.append(triplet[2])



plt.scatter(x, y, c=rugo, cmap='viridis')
plt.colorbar()
plt.show()