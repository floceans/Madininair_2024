"""
@description: Fonctions utilisées par ruf_maker.py
@author: Florent Puy
@date: 5 août 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from colorama import Fore, Back, Style, init
from scipy.ndimage import uniform_filter
from math import *

from scipy.ndimage import zoom
from matplotlib.image import imread, imsave

init()


def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
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
    
def recadrer(matrice):
    # retirer lignes du haut
    for k in range(0, 333):
        matrice.pop(0)

    #retirer lignes du bas
    for k in range(0, 0):
        matrice.pop(-1)

    # retirer colonne droite
    for k in range(0, 100):
        for l in range(len(matrice)):
            matrice[l].pop(-1)

    # retirer colonne gauche
    for k in range(0, 233):
        for l in range(len(matrice)):
            matrice[l].pop(0)
    return matrice

def traiter_alti(alti):
    for k in tqdm(range(len(alti)), desc=f"{Fore.MAGENTA}Traitement du fichier{Style.RESET_ALL}", 
                  bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.MAGENTA, Style.RESET_ALL)):
        for l in range(len(alti)):
            if alti[k][l] == -99999.00 or alti[k][l]<0: # mettre à 0 données non existantes et mer
                alti[k][l] = 0.0


def smooth_matrix(matrix, size=20):

    matrix = np.array(matrix, dtype=float)  # Convertir en numpy array pour faciliter les calculs
    
    # Appliquer un filtre uniforme de taille `size`
    smoothed = uniform_filter(matrix, size=size, mode='nearest')
    
    return smoothed.tolist()

def rugo_maker(ruf):
    m = len(ruf)
    n = len(ruf[0])

    # Initialisation correcte de rugo
    rugo = [[0]*n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            # Assurez-vous que chaque élément de ruf[i][j] a bien la bonne longueur avant d'utiliser pop()
            if len(ruf[i][j]) > 3:
                ruf[i][j].pop(3)  # Suppression du quatrième élément si présent

            # Comparaison des couleurs
            if ruf[i][j] == [230, 242, 255]:  # mer
                rugo[i][j] = 0.0001
            elif ruf[i][j] == [255, 0, 0]:  # rouge // discontinuous urban traffic
                rugo[i][j] = 0.5
            elif ruf[i][j] == [166, 242, 0]:  # vert clair // little tree forest
                rugo[i][j] = 0.6
            elif ruf[i][j] == [166, 230, 77]:  # vert foncé // transitionnal woodland-shrubland
                rugo[i][j] = 0.03
            elif ruf[i][j] == [242, 166, 77]:  # orange(à gauche) // banana / sugar cane plantation
                rugo[i][j] = 0.1
            elif ruf[i][j] == [255, 230, 77]:  # jaune centre bas // complex cultivation patterns
                rugo[i][j] = 0.3
            elif ruf[i][j] == [230, 230, 77]:  # jaune verdâtre // natural grassland
                rugo[i][j] = 0.03
            elif ruf[i][j] == [230, 204, 77]:  # marron clair (en bas à gauche) // mostly agriculture fields
                rugo[i][j] = 0.3
    return rugo

def parse_coordinates(file_path):
    # Crée un dictionnaire pour stocker les coordonnées par numéro de ligne
    points = []
    
    lat_antes = 0
    long_antes = 0
    
    k = 0
    
    with open(file_path, 'r') as file:
        for line in file:
            # Nettoie et découpe la ligne
            line = line.strip()
            parts = line.split(',')

            # Extraire les données
            #line_number = int(parts[0])
            latitude = float(parts[1])
            longitude = float(parts[2])
            # altitude = float(parts[3]) # Non utilisé dans la sortie

            # Ajouter les coordonnées à la liste correspondante
            if latitude == lat_antes and longitude == long_antes:
                continue
            
            elif longitude == long_antes:
                points[-1].append([latitude, longitude])
            
            elif longitude != long_antes and k != 0:
                points.append([[latitude, longitude]])
            elif k == 0:
                points.append([[latitude, longitude]])
            
            lat_antes = latitude
            long_antes = longitude
            

    return points


def read_file(file_path):
    M = []
    with open(file_path, 'r') as file:
        for line in file:
            # Nettoie et découpe la ligne
            line = line.strip()
            parts = line.split(',')

            # Extraire les données
            line_number = int(parts[0])
            latitude = float(parts[1])
            longitude = float(parts[2])
            M.append([line_number, latitude, longitude])
            
    return M


def matrice_en_liste(matrice):
    # Convertir la matrice en une liste de valeurs
    liste = []
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            liste.append(matrice[i][j])
    
    return liste


def liste_en_matrice(liste):
    # Calculer la taille de la matrice carrée nécessaire
    taille = len(liste)
    taille_matrice = int(sqrt(taille))
    
    # Créer la matrice carrée sans la dernière ligne incomplète
    matrice = []
    for i in range(taille_matrice):
        ligne = []
        for j in range(taille_matrice):
            index = i * taille_matrice + j
            if index < taille:
                ligne.append(liste[index])
        if len(ligne) == taille_matrice:
            matrice.append(ligne)
    
    return matrice


def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = [[matrix[j][i] for j in range(rows)] for i in range(cols)]
    return transposed



def redimensionner_image(image_path, i, j, output_path):

    # Lire l'image
    image = imread(image_path)
    
    # Obtenir les dimensions originales
    hauteur_originale, largeur_originale = image.shape[:2]
    
    # Calculer les facteurs de redimensionnement
    facteur_hauteur = i / hauteur_originale
    facteur_largeur = j / largeur_originale
    
    # Redimensionner l'image en utilisant scipy.ndimage.zoom
    if image.ndim == 3:
        image_redimensionnee = np.zeros((i, j, image.shape[2]), dtype=np.float32)
        for k in range(image.shape[2]):
            image_redimensionnee[:, :, k] = zoom(image[:, :, k], (facteur_hauteur, facteur_largeur), order=3)
    else:
        image_redimensionnee = zoom(image, (facteur_hauteur, facteur_largeur), order=3)
    
    # Normaliser les valeurs de l'image redimensionnée dans la plage [0, 1]
    image_redimensionnee = np.clip(image_redimensionnee, 0, 1)
    
    # Sauvegarder l'image redimensionnée
    imsave(output_path, image_redimensionnee)
    
    return image_redimensionnee

