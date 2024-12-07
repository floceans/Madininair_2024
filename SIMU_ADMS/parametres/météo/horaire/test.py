def extract_date_time(date_string):
    
    # Extraire chaque composante en utilisant le découpage de chaîne
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    hour = int(date_string[8:10])

    return year, month, day, hour


from datetime import datetime

def day_of_year(month, day):
    # Créer une date pour l'année actuelle avec le mois et le jour spécifiés
    date = datetime(datetime.now().year, month, day)

    # Extraire le jour de l'année à partir de la date créée
    day_of_year = date.timetuple().tm_yday

    return day_of_year
def convertisseur_jcm2_wm2(jcm2):
    alpha = 100/36
    return jcm2*alpha

from datetime import datetime, timedelta

def avancer_temps(annee, jour, heure):
    # Créer une date de base en début d'année
    date_base = datetime(annee, 1, 1)
    
    # Ajouter le jour et l'heure donnés
    date_actuelle = date_base + timedelta(days=jour - 1, hours=heure - 1)
    
    # Ajouter 4 heures
    nouvelle_date = date_actuelle + timedelta(hours=4)
    
    # Extraire la nouvelle année, jour et heure
    nouvelle_annee = nouvelle_date.year
    nouvelle_jour = (nouvelle_date - datetime(nouvelle_date.year, 1, 1)).days + 1
    nouvelle_heure = nouvelle_date.hour + 1  # Ajuster l'heure pour être de 1 à 24
    
    return nouvelle_annee, nouvelle_jour, nouvelle_heure

# Exemple d'utilisation
annee, jour, heure = 2023, 111, 22
nouvelle_annee, nouvelle_jour, nouvelle_heure = avancer_temps(annee, jour, heure)
print(f"Nouvelle date et heure: {nouvelle_annee}, jour {nouvelle_jour}, heure {nouvelle_heure}")
