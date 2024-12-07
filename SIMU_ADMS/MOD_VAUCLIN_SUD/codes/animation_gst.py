import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

# Lire les données à partir du fichier texte
def read_data(file_path):
    rows = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Essayer de lire et de traiter chaque ligne
                parts = line.strip().split(',')
                #if len(parts) != 7:
                #    raise ValueError("Nombre incorrect de colonnes : ", len(parts))
                
                # Extraire les valeurs avec gestion des erreurs
                année = int(parts[0].strip())
                jour = int(parts[1].strip())
                heure = int(parts[2].strip())
                latitude = float(parts[4].strip())
                longitude = float(parts[5].strip())
                data = float(parts[-1].strip())

                rows.append([heure, latitude, longitude, data])
            except (ValueError, IndexError, TypeError) as e:
                print(f"Erreur lors du traitement de la ligne : {line.strip()}")
                #print(f"Message d'erreur : {e}")

    # Convertir les lignes en DataFrame
    df = pd.DataFrame(rows, columns=['heure', 'latitude', 'longitude', 'data'])
    return df

# Fonction pour organiser les données par heure
def organize_by_hour(data):
    data = data[data['heure'].between(4, 23)]  # Filtrer les heures entre 4 et 23
    grouped = data.groupby('heure')
    return grouped

# Trouver les limites globales de la colorbar
def get_color_limits(data):
    return data['data'].min(), data['data'].max()

# Fonction pour mettre à jour l'animation
def update(frame):
    heure_debut = 4
    plt.clf()
    hour = frame + heure_debut
    current_data = times.get(hour, pd.DataFrame())
    ## cmap='YlOrBr'
    sc = plt.scatter(current_data['latitude'], current_data['longitude'], c=current_data['data'], 
                     cmap='viridis', marker = '.', s=60, edgecolor='None')#, vmin=color_limits[0], vmax=color_limits[1])
    plt.xlim(data['latitude'].min() - 1, data['latitude'].max() + 1)
    plt.ylim(data['longitude'].min() - 1, data['longitude'].max() + 1)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title(f'Hour: {hour}')
    # Ajouter la barre de couleur
    plt.colorbar(sc, label='Data Value')

# Lire les données
file_path = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\MOD_FRANCOIS\test_2_Le_francois.gst'  # Remplace par le chemin de ton fichier
data = read_data(file_path)

# Organiser les données par heure
grouped_data = organize_by_hour(data)

# Préparer les heures pour l'animation
times = {hour: group for hour, group in grouped_data}

# Trouver les limites globales pour la colorbar
color_limits = get_color_limits(data)

# Créer la figure pour l'animation
fig = plt.figure()

# Créer l'animation
ani = animation.FuncAnimation(fig, update, frames=22, repeat=False, interval=500)

# Afficher l'animation
plt.show()
