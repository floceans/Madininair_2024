import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Initialiser les listes pour stocker les données
times = []
sensor_readings = []
avg = 0
zcc = -1
avant = 7
apres = 175

# Charger le fichier CSV
csv_file = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\2024_08_14-20_data_francois\Thalemont.csv'  # Remplacez par le chemin de votre fichier CSV
with open(csv_file, mode='r') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Sauter l'en-tête du fichier CSV

    # Lire les données ligne par ligne
    for row in reader:
        zcc += 1
        utc_datetime_str = row[3]  # Colonne UTC_DateTime
        sensor_1_reading_str = row[21]  # Colonne Sensor_1_Reading

        # Convertir UTC_DateTime en objet datetime
        utc_datetime = datetime.strptime(utc_datetime_str, '%Y-%m-%d %H:%M:%S')

        # Convertir Sensor_1_Reading en float
        try :
            sensor_1_reading = float(sensor_1_reading_str)
            if sensor_1_reading <= 0:
                sensor_1_reading= 0.25
                #continue
        except ValueError:
            continue
        
        # Ajouter les valeurs aux listes
        times.append(utc_datetime)
        sensor_readings.append(sensor_1_reading)
        if avant < zcc < apres :
            avg += sensor_1_reading

print(f"Nombre de mesures : {len(sensor_readings)}, Moyenne : {avg/(apres - avant)}") #len(sensor_readings)

# Afficher les valeurs en fonction du temps
plt.figure(figsize=(10, 6))
plt.plot(times, sensor_readings, marker='', linestyle='-')
plt.xlabel('UTC DateTime')
plt.ylabel('Sensor 1 Reading (ppm)')
plt.title('Sensor 1 Reading Over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()



