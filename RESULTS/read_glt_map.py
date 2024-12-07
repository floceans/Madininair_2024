import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np
from shapely.geometry import Point
from read_glt import *
from tqdm import tqdm
from colorama import Fore, Style
from collorbar import color_madininair

# Étape 1: Créer un GeoDataFrame pour la Martinique avec des coordonnées spécifiques
# (Exemple : on place quelques points aléatoires sur la Martinique avec des valeurs associées)

# Création de quelques points aléatoires en Martinique avec des valeurs associées

filepath =  r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\MOD_ROBERT\MOD_ROBERT.glt'

x, y, data = read_data_from_file(filepath)

print(x[0], y[0], data[0])  

for k in tqdm(range(len(x)), desc='Convertion coord en epsg 4326', unit='points', colour='magenta'):
    lon, lat = convert_epsg3395_to_epsg4326(x[k], y[k])
    x[k] = lon
    y[k] = lat

data = {
    'latitude': y,
    'longitude': x,
    'value': data  # Valeurs associées aux points
}

# Conversion en GeoDataFrame
gdf = gpd.GeoDataFrame(
    data, 
    geometry=[Point(xy) for xy in zip(data['longitude'], data['latitude'])],
    crs="EPSG:4326"  # Système de coordonnées géographiques
)

# Étape 2: Reprojection en Web Mercator (EPSG:3857) pour correspondre aux tuiles OSM
gdf = gdf.to_crs(epsg=3857)

# Étape 3: Création de la carte avec contextily
fig, ax = plt.subplots(figsize=(10, 10))


# Affichage des points avec une échelle de couleur basée sur la valeur
sc = gdf.plot(
    ax=ax,
    alpha=0.6, 
    column='value', 
    cmap=color_madininair, #'YlOrRd','turbo'  # Palette de couleurs
    markersize=20,  # Taille des points
    legend=True, 
    legend_kwds={'label': "Concentration H2S (ppm)"}
)

# Ajouter les tuiles OpenStreetMap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)



# Ajuster les limites de la carte pour englober tous les points
ax.set_xlim(gdf.geometry.x.min() - 100, gdf.geometry.x.max() + 100)
ax.set_ylim(gdf.geometry.y.min() - 100, gdf.geometry.y.max() + 100)

# Afficher la colorbar
#cbar = plt.colorbar(sc.collections[0], ax=ax)
#cbar.set_label("Valeur associée")

# Afficher la carte
plt.show()
