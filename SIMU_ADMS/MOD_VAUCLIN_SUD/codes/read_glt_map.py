import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np
from shapely.geometry import Point
from read_glt import *
from tqdm import tqdm
from matplotlib.tri import Triangulation
from collorbar import color_madininair
from scipy.spatial import distance

# Étape 1: Lire les données du fichier
filepath = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\MOD_VAUCLIN_SUD\Vauclin_sud.glt'

x, y, data = read_data_from_file(filepath)

# Conversion des coordonnées en EPSG:4326
for k in tqdm(range(len(x)), desc='Conversion coord en EPSG:4326', unit='points', colour='magenta'):
    lon, lat = convert_epsg3395_to_epsg4326(x[k], y[k])
    x[k] = lon
    y[k] = lat

# Création d'un GeoDataFrame
data_dict = {
    'latitude': y,
    'longitude': x,
    'value': data
}

gdf = gpd.GeoDataFrame(
    data_dict,
    geometry=[Point(xy) for xy in zip(data_dict['longitude'], data_dict['latitude'])],
    crs="EPSG:4326"
)

# Reprojection en Web Mercator (EPSG:3857)
gdf = gdf.to_crs(epsg=3857)

# Définir une distance seuil (par exemple, 500 mètres)
distance_seuil = 150  # en unités de Web Mercator (mètres)

# Fonction pour filtrer les triangles dont les points sont trop éloignés
def filtrer_triangles(triangulation, points, seuil):
    mask = np.ones(triangulation.triangles.shape[0], dtype=bool)
    
    for i, triangle in enumerate(triangulation.triangles):
        # Récupérer les trois sommets du triangle
        pts = points[triangle]
        
        # Calculer les distances entre les trois points
        dist = distance.pdist(pts)
        
        # Si l'une des distances est supérieure au seuil, on masque ce triangle
        if np.any(dist > seuil):
            mask[i] = False
            
    return mask

# Création de la carte
fig, ax = plt.subplots(figsize=(10, 10))

# Vérifier s'il y a assez de points pour l'interpolation
if len(gdf) < 3:
    print("Pas assez de points pour l'interpolation.")
else:
    # Triangulation de Delaunay
    points = np.vstack([gdf.geometry.x, gdf.geometry.y]).T
    triang = Triangulation(gdf.geometry.x, gdf.geometry.y)
    
    # Filtrer les triangles trop grands
    mask = filtrer_triangles(triang, points, distance_seuil)
    triang.set_mask(~mask)

    levels = [0, 0.03, 0.07, 0.5, 1.5, 3, 5]

    # Affichage de la surface interpolée
    im = ax.tricontourf(triang, gdf['value'], cmap=color_madininair, levels=levels, alpha=0.6)

    # Créer une colorbar avec les niveaux ajustés
    cbar = plt.colorbar(im, ax=ax, label="Concentration H2S (ppm)", ticks=levels)
    cbar.set_label("Concentration H2S (ppm)")
    
# Ajouter les tuiles OpenStreetMap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Ajuster les limites de la carte pour englober tous les points
ax.set_xlim(gdf.geometry.x.min() - 50, gdf.geometry.x.max() + 150)
ax.set_ylim(gdf.geometry.y.min() - 50, gdf.geometry.y.max() + 50)

# Afficher la carte
plt.title("Carte de concentration H2S")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.savefig('carte_H2S_long_3.png', dpi=600, bbox_inches='tight', transparent=True)

plt.show()