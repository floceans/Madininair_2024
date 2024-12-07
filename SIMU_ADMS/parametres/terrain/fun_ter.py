"""
@description: Fonction utilisée par ter_maker_from_xyz.py
@author: Florent Puy
@date: 5 août 2024
"""


import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from colorama import Fore, Back, Style, init
from pyproj import Proj, Transformer


def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in tqdm(file, desc=f"{Fore.MAGENTA}Lecture du fichier{Style.RESET_ALL}"):
            # Convert the line into a list of integers
            row = list(map(float, line.split()))
            data.append(row)
    return data



def concat_matrices_ligne(matrix1, matrix2):
    # Vérifier si les deux matrices ont le même nombre de lignes
    if len(matrix1) != len(matrix2):
        raise ValueError("Les matrices doivent avoir le même nombre de lignes.")
    
    # Concaténer les matrices ligne par ligne
    concatenated_matrix = []
    for row1, row2 in zip(matrix1, matrix2):
        concatenated_matrix.append(row1 + row2)
    
    return concatenated_matrix

def concat_matrices_colonne(matrix1, matrix2):
    # Vérifier si les deux matrices ont le même nombre de colonnes
    if len(matrix1) != len(matrix2):
        raise ValueError("Les matrices doivent avoir le même nombre de lignes.")
    
    
    return matrix1 + matrix2


## afficher matrice ##
def show_matrix(matrix):
    # Convertir la matrice en tableau numpy
    np_matrix = np.array(matrix)
    
    # Afficher la matrice
    print(np_matrix)
    np.shape(np_matrix)



from pyproj import Proj, Transformer

def convert_utm20_to_epsg3395(x, y):

    # Définir la projection UTM Zone 20N avec WGS 84
    proj_utm20 = Proj(proj='utm', zone=20, ellps='WGS84', north=True)
    
    # Définir la projection EPSG:3395 (WGS 84 / Mercator (auxiliary sphere))
    proj_epsg3395 = Proj(proj='merc', lon_0=0, x_0=0, y_0=0, ellps='WGS84')

    # Créer un transformateur pour convertir les coordonnées
    transformer = Transformer.from_proj(proj_utm20, proj_epsg3395)

    # Convertir les coordonnées
    lon, lat = transformer.transform(x, y)

    return lat, lon


def tracer_alti_vs_lati_longi_2D(liste_alti, liste_longi, liste_lati):
    """
    Trace un graphique 2D de l'altitude en fonction de la latitude et de la longitude,
    avec une colorbar représentant les valeurs d'altitude.

    Args:
        liste_alti (list): Liste des altitudes.
        liste_longi (list): Liste des longitudes.
        liste_lati (list): Liste des latitudes.
    """
    if not (len(liste_alti) == len(liste_longi) == len(liste_lati)):
        raise ValueError("Les listes doivent avoir la même longueur.")

    # Convertir les listes en tableaux numpy pour une meilleure gestion
    x = np.array(liste_longi)
    y = np.array(liste_lati)
    z = np.array(liste_alti)

    # Création du graphique
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(x, y, z, cmap='viridis', s=100, edgecolor='k')

    # Ajouter des labels et un titre
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Altitude en fonction de la Latitude et de la Longitude')

    # Ajouter une barre de couleur pour indiquer les valeurs d'altitude
    cbar = plt.colorbar(scatter)
    cbar.set_label('Altitude')

    # Afficher le graphique
    plt.show()