import csv
from datetime import datetime
import matplotlib.pyplot as plt

import csv
from datetime import datetime
import matplotlib.pyplot as plt

def plot_data(file_path, zones):
    """
    Lit les données depuis un fichier CSV, filtre par site et polluant H2S, 
    puis trace les courbes des mesures pour chaque site.
    
    Arguments:
    file_path -- Chemin du fichier source CSV.
    """
    
    avg = 0
    n = 0
    zone_empty = False
    
    if zones == []:
        zone_empty = True
        
    # Initialisation d'un dictionnaire pour stocker les données par site
    data_by_site = {}
    
    # Nom du site à afficher sur le graphique
    #site = 'Frégate EST 2'

    # Lecture du fichier CSV
    with open(file_path, mode='r') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)  # Lire l'en-tête (ligne 1)
        
        # Index des colonnes pertinentes
        nom_idx = header.index('nom')
        date_idx = header.index('date')
        mesure_idx = header.index('mesure')
        polluant_idx = header.index('polluant')
        
        for row in reader:
            site_name = row[nom_idx]
            
            if zone_empty:
                zones.append(site_name)
            
            # Filtrer les sites
            if site_name not in zones:
                continue
            
            polluant = row[polluant_idx]
            
            # Filtrer les données pour ne garder que celles de H2S
            if polluant != 'H2S':
                continue
            
            # Convertir les valeurs de date et mesure
            date = datetime.strptime(row[date_idx], '%Y-%m-%d %H:%M:%S.%f')
            mesure = float(row[mesure_idx])
            
            # Ajouter les données au dictionnaire
            if site_name not in data_by_site:
                data_by_site[site_name] = {'dates': [], 'mesures': []}
            
            data_by_site[site_name]['dates'].append(date)
            data_by_site[site_name]['mesures'].append(mesure)
            
            n += 1
            avg += mesure

    print(f"Nombre de mesures : {n}, Moyenne : {avg/n}")
    
    # Tracer les courbes pour chaque site
    plt.figure(figsize=(10, 6))
    
    for site_name, site_data in data_by_site.items():
        plt.plot(site_data['dates'], site_data['mesures'], label=site_name)

    # Ajouter graphique
    plt.xlabel('Date')
    plt.ylabel('Mesure')
    plt.title('Mesures de H2S par site')
    plt.legend()
    plt.grid(True)
    


# Exemple d'utilisation
file_path_ppal = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\2024_08_14-20_data_francois\sarg_ppal_14_20_aout.csv'
zones = ["Dostaly Sud", "Frégate EST 2"]#, "Frégate EST 2", 'Pointe Faula', 'Presqu\'ile', 'Chateau Paille']
plot_data(file_path_ppal, zones)

file_path_compl = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\2024_08_14-20_data_francois\sarg_compl_14_20_aout.csv' 
zones = []
plot_data(file_path_compl, zones)

plt.show()