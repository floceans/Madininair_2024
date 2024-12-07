"""
@description : Créé fichier .ter à partir d'un fichier .xyz
@author : Florent Puy
@date : 5 août 2024
"""


from pyproj import Transformer
from tqdm import tqdm
from fun_ter import *
import numpy as np
import matplotlib.pyplot as plt

LIGHT = True ## Divise le nombre de points par 4, garde la meme couverture géographique

compress_factor = 3

liste_alti = []
liste_longi = []
liste_lati = []

# Définir les fichiers d'entrée et de sortie
input_file = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\terrain\CODE_PROPRE\data_XYZ\ffrancois_dostaly.xyz"
output_file = "Francois_dostaly_epsg3395.ter"

min = 0
max = 0

old_alti = 0
old_longi = 0
old_lati = 0

num_longi = 0
num_lati = 0


pass_ = 0

numero_ligne = 1
num_ligne_ecrite = 1
# Ouvrir le fichier d'entrée pour lecture et le fichier de sortie pour écriture
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in tqdm(infile, desc="Chargement", ncols=80, ascii=True):
        
        # Nettoyer et séparer les données
        parts = line.strip().split(' ')
        if len(parts) != 3:
            parts.append(old_alti)
        
        longitude, latitude, altitude = parts
        latitude = float(latitude)
        longitude = float(longitude)
        altitude = float(altitude)

        if altitude < 0:
            altitude = 0
        
        old_alti = altitude
        if old_lati != latitude:
            num_lati += 1
            old_lati = latitude
        
        if old_longi != longitude:
            num_longi += 1
            old_longi = longitude

        # pavage une ligne sur deux & une colonne sur deux
        if LIGHT and num_lati % 2 == 1 and num_longi % 2 == 0:
            pass_ += 1
                    
            if altitude > float(max):
                max = altitude
            elif altitude < float(min):
                min = altitude
            
            # pour plot après
            liste_alti.append(altitude)
            liste_longi.append(longitude)
            liste_lati.append(latitude)

            #ecriture
            altitude = f"{float(altitude):e}"
            outfile.write(f"{num_ligne_ecrite},{longitude},{latitude},{altitude}\n")
            numero_ligne += 1
            num_ligne_ecrite += 1
            
        elif LIGHT :
            numero_ligne += 1
            continue
        else:
            outfile.write(f"{numero_ligne},{latitude},{longitude},{altitude}\n")
            numero_ligne += 1

print(f"Les coordonnées ont été converties et sauvegardées dans {output_file}.", pass_)

print(f"Altitude min : {min}")
print(f"Altitude max : {max}")

# Tracé de alti

for k in range(len(liste_alti)):
    liste_alti[k] = float(liste_alti[k])
    
    

plt.scatter(liste_longi, liste_lati, c=liste_alti, cmap='viridis', s=1)
plt.colorbar(label='Altitude')
plt.title('Altitude')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

#3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(liste_longi, liste_lati, liste_alti, c=liste_alti, cmap='viridis')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude')


plt.show()
