import csv
from datetime import datetime
import matplotlib.pyplot as plt

def lire_et_calculer_moyenne(fichier):
    total_concentration = 0
    count = 0
    data_points = []

    try:
        with open(fichier, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            
            # Ignorer les deux premières lignes
            next(reader)
            next(reader)
            
            for row in reader:
                try:
                    # Extraire la date et l'heure
                    date_str = row[0]
                    concentration = float(row[1])
                    
                    # Convertir la chaîne de date en objet datetime
                    date_obj = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
                    heure = date_obj.hour
                    
                    # Filtrer les heures entre 19h00 et 08h00
                    if heure >= 13 or heure < 17:
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

# Utilisation des fonctions
bdm = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\9_25_08_fregate_bdm.csv"
maison = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\09_25_fragate_maison.csv"

FaC = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Robert\FaC_09_25_08_24.csv"
Pontalery = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Robert\09_25_08_24_Pontalery.csv"

moyenne_bdm, data_bdm = lire_et_calculer_moyenne(bdm)
moyenne_maison, data_maison = lire_et_calculer_moyenne(maison)
moyenne_fac, data_fac = lire_et_calculer_moyenne(FaC)
moyenne_pontalery, data_pontalery = lire_et_calculer_moyenne(Pontalery)

print("\n")

if moyenne_bdm is not None:
    moyenne_bdm_ppm = moyenne_bdm / 1000  # Convertir en ppm si nécessaire
    print(f"La moyenne des concentrations entre 19h00 et 08h00 est de {moyenne_bdm_ppm} ppm à BDM.")
    afficher_donnees(data_bdm, "Concentrations à BDM")
print("\n")

if moyenne_maison is not None:
    print(f"La moyenne des concentrations entre 19h00 et 08h00 est de {moyenne_maison/1000} ppm à Maison.")
    afficher_donnees(data_maison, "Concentrations à Maison")
print("\n")

if moyenne_fac is not None:
    print(f"La moyenne des concentrations entre 19h00 et 08h00 est de {moyenne_fac/1000} ppm à FaC.")
    afficher_donnees(data_fac, "Concentrations à FaC")
print("\n")
 
if moyenne_pontalery is not None:
    print(f"La moyenne des concentrations entre 19h00 et 08h00 est de {moyenne_pontalery/1000} ppm à Pontalery.")
    afficher_donnees(data_pontalery, "Concentrations à Pontalery")