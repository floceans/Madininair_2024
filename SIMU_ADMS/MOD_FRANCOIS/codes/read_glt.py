import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import contextily as ctx
from pyproj import Transformer



def read_data_from_file(filename):
    x_values = []
    y_values = []
    data_values = []
    bool_scale = False
    
    with open(filename, 'r') as file:
        for line in file:
            # Nettoyer la ligne pour supprimer les espaces inutiles et diviser en colonnes
            parts = line.strip().split(',')
            if len(parts) <= 5:
                try:
                    x = float(parts[0].strip())
                    y = float(parts[1].strip())
                    z = float(parts[2].strip())
                    data1 = float(parts[3].strip())
                    #data2 = float(parts[4].strip())
                    
                    # Concaténer les deux valeurs data si nécessaire
                    data = data1 #(data1 + data2) / 2
                    
                    # Ajouter les valeurs aux listes


                    if data > 5 : data = 5
                    
                    if data > 0.03 and bool_scale : 
                        data_values.append(data)
                        x_values.append(x)
                        y_values.append(y)
                    
                    if not bool_scale : 
                        #data_values.append(data)
                        #x_values.append(x)
                        #y_values.append(y)
                        bool_scale = True
                    
                except ValueError:
                    print(f"Skipping line due to conversion error: {line.strip()}")
        #data_values[0] = -0.5
    
    return x_values, y_values, data_values



def plot_data(x_values, y_values, data_values):
    print('paaaaaaaaaaaaaaassssssssssssssss')
    plt.figure(figsize=(10, 6))
    for k in range(len(x_values)):
        lon, lat = convert_epsg3395_to_epsg4326(x_values[k], y_values[k])
        x_values[k] = lon
        y_values[k] = lat
    scatter = plt.scatter(x_values, y_values, alpha = 0.4, c=data_values, cmap='jet', marker='o', s=30, edgecolor='None')
    
    # Ajouter une barre de couleur pour montrer l'échelle des valeurs
    plt.colorbar(scatter, label='Data Value')
    
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Scatter Plot of Data by X and Y Coordinates')
    plt.grid(True)
    plt.show()


def convert_epsg3395_to_epsg4326(x, y):
    transformer = Transformer.from_crs("epsg:3395", "epsg:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat
      


#filename = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\MOD_FRANCOIS\test_2_Le_francois.glt'
#x_values, y_values, data_values = read_data_from_file(filename)
#plot_data(x_values, y_values, data_values)

#plt.show()