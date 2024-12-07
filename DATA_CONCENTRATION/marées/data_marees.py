import csv
from datetime import *
import matplotlib.pyplot as plt

def lire_et_calculer_moyenne(fichier, filtered_dates):
    total_concentration = 0
    count = 0
    data_points = []

    try:
        with open(fichier, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            
            # Ignorer les deux premières lignes
            next(reader)
            next(reader)
            bool = False
            
            for row in reader:
                try:
                    # Extraire la date et l'heure
                    date_str = row[0]
                    concentration = float(row[1])
                    
                    # Convertir la chaîne de date en objet datetime
                    date_obj = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
                    
                    #print('filtered_dates:', filtered_dates)
                    i = 0
                    
                    for date in filtered_dates:
                        #print('date_obj : ', date_obj)
                        #print('date : ', date)
                        #print('diff : ', (date_obj - date))
                        if (date_obj - date) < timedelta(hours=1): ######################## condition qui chie ###########################&=
                            #print('iciii')
                            bool = True
                            i += 1
                        else:
                            bool = False
                    if bool:
                        #print('paaaaaaaaassssssss')
                        total_concentration += concentration
                        count += 1
                        data_points.append((date_obj, concentration))
                except ValueError as ve:
                    print(f"Erreur de conversion de données sur la ligne {row}: {ve}")
        
        # Calculer la moyenne
        if count > 0:
            moyenne_concentration = total_concentration / count
        else:
            moyenne_concentration = 0

        return moyenne_concentration, data_points

    except FileNotFoundError:
        print(f"Le fichier {fichier} n'a pas été trouvé.")
        return None, []
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier {fichier}: {e}")
        return None, []



# Fonction pour afficher les données avec matplotlib
def afficher_donnees(data_points, titre):
    if data_points:
        dates, concentrations = zip(*data_points)
        plt.figure(figsize=(10, 5))
        plt.plot(dates, concentrations)
        plt.title(titre)
        plt.xlabel("Date")
        plt.ylabel("Concentration (ppb)")
        plt.grid(True)
        #plt.show()
    else:
        print("Aucune donnée à afficher.")
        
def parse_data(file_content):
    data = []
    for line in file_content.splitlines():
        # Skip comment lines
        if line.startswith("#"):
            continue
        
        # Split each data row into date, value, and source
        row = line.split(";")
        if len(row) == 3:
            date = datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S')
            value = float(row[1])
            source = int(row[2])
            data.append((date, value, source))
    
    return data

# Function to filter dates based on conditions
def filter_dates_by_value(data, lower_bound, upper_bound):
    filtered_dates = []
    k = 0
    for entry in data:
        date, value, _ = entry
        if (value < lower_bound) and (k%60 == 0):
            filtered_dates.append(date)
        k += 1
    return filtered_dates

# Function to read and parse the file
def read_and_parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        return parse_data(file_content)


file_path = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\marées\224_2024.txt'

# Read and parse the file
parsed_file_data = read_and_parse_file(file_path)

# Define the bounds for filtering (data < 0.5 or data > 0.8)
lower_bound = 0.5
upper_bound = 0.8

# Filter the dates based on the given condition
filtered_dates = filter_dates_by_value(parsed_file_data, lower_bound, upper_bound)

print('filtered_dates : ', filtered_dates)




# Utilisation des fonctions
bdm = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\9_25_08_fregate_bdm.csv"
maison = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\09_25_fragate_maison.csv"

FaC = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Robert\FaC_09_25_08_24.csv"
Pontalery = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Robert\09_25_08_24_Pontalery.csv"

moyenne_bdm, data_bdm = lire_et_calculer_moyenne(bdm, filtered_dates)
moyenne_maison, data_maison = lire_et_calculer_moyenne(maison, filtered_dates)
moyenne_fac, data_fac = lire_et_calculer_moyenne(FaC, filtered_dates)
moyenne_pontalery, data_pontalery = lire_et_calculer_moyenne(Pontalery, filtered_dates)

print("\n")

if moyenne_bdm is not None:
    moyenne_bdm_ppm = moyenne_bdm / 1000  # Convertir en ppm si nécessaire
    print(f"La moyenne des concentrations à marée haute est de {moyenne_bdm_ppm} ppm à BDM.")
    afficher_donnees(data_bdm, "Concentrations à BDM")
print("\n")

if moyenne_maison is not None:
    print(f"La moyenne des concentrations à marée haute est de {moyenne_maison/1000} ppm à Maison.")
    afficher_donnees(data_maison, "Concentrations à Maison")
print("\n")

if moyenne_fac is not None:
    print(f"La moyenne des concentrations à marée haute est de {moyenne_fac/1000} ppm à FaC.")
    afficher_donnees(data_fac, "Concentrations à FaC")
print("\n")
 
if moyenne_pontalery is not None:
    print(f"La moyenne des concentrations à marée haute est de {moyenne_pontalery/1000} ppm à Pontalery.")
    afficher_donnees(data_pontalery, "Concentrations à Pontalery")


#superposer marees et BDM
