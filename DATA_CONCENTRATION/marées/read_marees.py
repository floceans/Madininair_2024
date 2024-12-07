import matplotlib.pyplot as plt
import datetime as datetime
import csv
from datetime import datetime, timedelta
  


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
    
    

# Function to parse the data from the file content
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
        if (value < lower_bound or value > upper_bound) and (k%60 == 0):
            filtered_dates.append((date, value))
        k += 1
    return filtered_dates

# Function to read and parse the file
def read_and_parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        return parse_data(file_content)

# Path to the file
file_path = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\marées\224_2024.txt'

# Read and parse the file
parsed_file_data = read_and_parse_file(file_path)

# Define the bounds for filtering (data < 0.5 or data > 0.8)
lower_bound = 0.5
upper_bound = 0.8

# Filter the dates based on the given condition
filtered_dates = filter_dates_by_value(parsed_file_data, lower_bound, upper_bound)

# Extract dates and values for plotting
dates = [entry[0] for entry in parsed_file_data]
values = [entry[1] for entry in parsed_file_data]

# Extract filtered dates and values
filtered_dates_values = [entry[0] for entry in filtered_dates]
filtered_values = [entry[1] for entry in filtered_dates]



# CONCENTRATION #
bdm = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\9_25_08_fregate_bdm.csv"
maison = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Francois\09_25_fragate_maison.csv"

FaC = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Robert\FaC_09_25_08_24.csv"
Pontalery = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\data_concentrations\Robert\09_25_08_24_Pontalery.csv"

moyenne_bdm, data_bdm = lire_et_calculer_moyenne(Pontalery, dates)

print("moyenne_bdm : ", moyenne_bdm)
print("data_bdm : ", data_bdm)




# Plotting the data using matplotlib
plt.figure(figsize=(10, 6))

# Plot all data
for k in range (len(values)):
    values[k] = values[k]-0.6

plt.plot(dates, values, label='Valeur', marker='o',markersize = 1, color='blue')

#plot bdm
plt.plot([date for date, _ in data_bdm][70:], [concentration/7000 for _, concentration in data_bdm][70:], color='green', label='Concentration', zorder=5)


# Highlight the filtered data points
for k in range (len(filtered_values)):
    filtered_values[k] = filtered_values[k]-0.6
#plt.scatter(filtered_dates_values, filtered_values, color='red', label='Data < 0.5 or > 0.8', zorder=5)


# Adding titles and labels
plt.title('Concentration sur marées')
plt.xlabel('Temps')
plt.ylabel('Valeur (m & ppm)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()

# Show the plot
plt.show()

# Print the filtered dates
print("Dates where data < 0.5 or data > 0.8:")
for date, value in filtered_dates:
    print(f"Date: {date}, Valeur: {value}")
    
print(len(filtered_dates))
