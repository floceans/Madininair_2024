import requests
import matplotlib.pyplot as plt
import json
import urllib3
from datetime import datetime, timedelta
import pytz
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import module en local
from config import URL_XR_V2, ANNEE_ENVOI_INITIAL, print_dico

class Xr(object):

    def __init__(self):
        # Paramètres de connexion à XR
        self.sitesUrl = URL_XR_V2 + "/sites?"
        self.mesuresUrl = URL_XR_V2 + "/measures?"
        self.dataUrl = URL_XR_V2 + "/data?"
        self.s = requests.Session()
        
        # Config logique
        self.anneeInitial = ANNEE_ENVOI_INITIAL
        ## H2S ID = 05
        self.listeIdsPolluants = ['01', '02', '03', '04', '05', '08', '12', '21', '22', '23', '24', '39', '51', '52', '53', '54', '58', '60', '68', 'S5', 'S7'] # Se retrouve à l'aide de l'API: https://172.16.49.33:8443/dms-api/public/v1/physicals

        

    def get_data_from_period(self, dType, listeMesures, dDebut, dFin):
        """Récupère les données entre deux dates renseignées

        Args:
            dataTypes (List): Type(s) de mesure (sta, hourly, daily, monthly, annual)
            listeMesures (List): Identifiant(s) des mesures à récupérer
            dDebut (String): Date de début
            dFin (String): Date de fin

        Returns:
            json: Contient les données retournées par l'API
        """

        # Découpage de la liste de mesures
        if len(listeMesures) > 1:
            params = ",".join(listeMesures)
        elif len(listeMesures) == 1:
            params = listeMesures[0]
        else:
            params = ""

        # Formatage de la date et de l'heure et de l'url
        westIndies_tz = pytz.timezone('America/Martinique')
        UTC_tz = pytz.utc
        date_debut_westIndies = westIndies_tz.localize(datetime.strptime(dDebut, '%Y-%m-%d'))
        date_fin_westIndies = westIndies_tz.localize(datetime.strptime(dFin, '%Y-%m-%d'))
        date_debut_UTC = date_debut_westIndies.astimezone(UTC_tz)
        date_fin_UTC = date_fin_westIndies.astimezone(UTC_tz)
        d_debut = 'from='+(date_debut_UTC + timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")
        d_fin = 'to='+(date_fin_UTC).strftime("%Y-%m-%dT%H:00:00Z")

        url = self.dataUrl+d_debut+'&'+d_fin+'&'+'measures='+params+'&dataTypes='+dType+'&validOnly=False'
        print(url)

        # Récupération des données
        self.s.verify = False
        data = self.s.get(url).json()
        return data
    
    def get_data_from_last_hours(self, dType='hourly', listeMesures=[], nHours=2):
        """Récupère les données pour les n dernières heures

        Args:
            dataTypes (List): Type(s) de mesure (sta, hourly, daily, monthly, annual)
            listeMesures (List): Identifiant(s) des mesures à récupérer
            nHours (Int): Nombre d'heure à récupérer depuis l'instant présent (1 < n < 168)

        Returns:
            json: Contient les données retournées par l'API
        """

        # Découpage de la liste de mesures
        if len(listeMesures) > 1:
            params = ",".join(listeMesures)
        elif len(listeMesures) == 1:
            params = listeMesures[0]
        else:
            params = ""

        # Formatage de l'url
        match dType:
            case 'sta':
                url = self.dataUrl+'includeRaw=true'+'&lastHours='+str(nHours)+'&measures='+params+'&dataTypes='+dType+'&validOnly=False'
            case _:
                url = self.dataUrl+'lastHours='+str(nHours)+'&measures='+params+'&dataTypes='+dType+'&validOnly=False'
        
        print(url)

        # Récupération des données
        self.s.verify = False
        data = self.s.get(url).json()
        return data
    
    def get_data_updated_since(self, dataTypes, listeMesures, dateSince):
        """Récupère les données depuis la date précisée

        Args:
            dataTypes (List): Type(s) de mesure (sta, hourly, daily, monthly, annual)
            listeMesures (List): Identifiant(s) des mesures à récupérer
            dateSince (String): Date à partir de laquelle il faut récupérer les données

        Returns:
            json: Contient les données retournées par l'API
        """
        # Decoupage de la liste de type de données
        if len(dataTypes) > 1:
            dTypes = ",".join(dataTypes)
        elif len(dataTypes) == 1:
            dTypes = dataTypes[0]
        else:
            dTypes = ""

        # Découpage de la liste de mesures
        if len(listeMesures) > 1:
            params = ",".join(listeMesures)
        elif len(listeMesures) == 1:
            params = listeMesures[0]
        else:
            params = ""

        # Formatage de la date et de l'heure et de l'url
        westIndies_tz = pytz.timezone('America/Martinique')
        UTC_tz = pytz.utc
        date_since_westIndies = westIndies_tz.localize(datetime.strptime(dateSince, '%Y-%m-%d'))
        date_since_UTC = date_since_westIndies.astimezone(UTC_tz)
        d_since = 'updatedSince='+(date_since_UTC + timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")

        url = self.dataUrl+d_since+'&'+'measures='+params+'&dataTypes='+dTypes+'&validOnly=False'
        print(url)

        # Récupération des données
        self.s.verify = False
        data = self.s.get(url).json()
        return data
    
    def get_sites(self):
        """Récupère la liste des sites à partir de l'année initiale renseignée dans la définition de la classe XR

        Returns:
            json: retourne la liste des données 
        """

        # Formatage de la date et de l'heure et de l'url pour tenir compte de la date initiale
        westIndies_tz = pytz.timezone('America/Martinique')
        UTC_tz = pytz.utc
        date_since_westIndies = westIndies_tz.localize(datetime.strptime(self.anneeInitial+'-01-01', '%Y-%m-%d'))
        date_since_UTC = date_since_westIndies.astimezone(UTC_tz)
        d_since = 'startDate='+(date_since_UTC + timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")
        
        url = self.sitesUrl+d_since
        print(url)

        dSites = self.s.get(url, verify=False).json()
        
        return dSites

    def get_mesures(self, listeMesures=['']):
        # Découpage de la liste de mesures
        if len(listeMesures) > 1:
            params = ",".join(listeMesures)
        elif len(listeMesures) == 1:
            params = listeMesures[0]
        else:
            params = ""
        
        # Découpage de la liste d'id de polluants
        physicals = ",".join(self.listeIdsPolluants)
        
        # Formatage de la date et de l'heure et de l'url pour tenir compte de la date initiale
        westIndies_tz = pytz.timezone('America/Martinique')
        UTC_tz = pytz.utc
        date_since_westIndies = westIndies_tz.localize(datetime.strptime(self.anneeInitial+'-01-01', '%Y-%m-%d'))
        date_since_UTC = date_since_westIndies.astimezone(UTC_tz)
        d_since = 'startDate='+(date_since_UTC + timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")

        url = self.mesuresUrl+'measures='+params+'&physicals='+physicals+'&'+d_since+'&validOnly=false'
        print(url)

        dMesures = self.s.get(url, verify=False).json()

        return dMesures





def afficher_sites(sites):
    for key, site_list in sites.items():
        try:
            print(f"Nombre de sites : {len(site_list)}")
            for site in site_list:
                print(f"Nom du site : {site['labelSite']}")
                print(f"Date de début : {site['startDate']}, Date de fin : {site['stopDate']}")
                print("-" * 40)
        except:
            print("Erreur lors de l'affichage des sites")
            print(site_list) 
            print("-" * 40)

def afficher_data(debut, fin, site, polluant):
    print(f"Date de début : {debut}, Date de fin : {fin}")
    print(f"Site : {site}")
    print(f"Polluant : {polluant}")
    print("-" * 40)


def afficher_data_horaire(data):
    if 'data' in data:
        for entry in data['data']:
            date_time = entry.get('date', 'N/A')
            value = entry.get('value', 'N/A')
            print(f"Date/Heure: {date_time}, Valeur: {value}")
    else:
        print("Aucune donnée disponible pour la période sélectionnée.")
        
        
def display_data(data):
    """
    Affiche un graphique des valeurs en fonction de la date à partir des données fournies.

    :param data: Le dictionnaire contenant les données horaires
    """
    try:
        # Extraction des données horaires
        hourly_data = data.get("data", [])[0].get("hourly", {}).get("data", [])
        
        if not hourly_data:
            print("Aucune donnée disponible.")
            return
        
        # Extraction des dates et des valeurs
        dates = []
        values = []

        for entry in hourly_data:
            date = entry.get("date")
            value = entry.get("value")
            
            if date and value is not None:  # S'assurer que les valeurs sont présentes
                dates.append(datetime.fromisoformat(date.replace("Z", "+00:00")))  # Conversion en objet datetime
                values.append(value)
        
        # Créer le graphique
        n = min(len(dates), len(values))
        plt.figure(figsize=(10, 6))
        plt.plot(dates[:n], values[:n], marker='o', linestyle='-', color='b', label='Valeurs')
        
        # Formatage du graphique
        plt.title("Valeurs en fonction de la date")
        plt.xlabel("Date")
        plt.ylabel("Valeur (ppb)")
        plt.xticks(rotation=45)  # Rotation des dates pour une meilleure lisibilité
        plt.tight_layout()  # Ajuste le graphique pour éviter le chevauchement
        plt.legend()
        plt.grid(True)
        
        # Afficher le graphique
        plt.show()
    
    except (TypeError, ValueError) as e:
        print(f"Erreur lors de l'affichage du graphique : {e}")


def tracer_valeurs(data):
    """
    Trace les valeurs selon les dates fournies dans le dictionnaire de données.

    :param data: Dictionnaire contenant les données à tracer.
    """
    # Initialiser les listes pour les dates et les valeurs
    dates = []
    valeurs = []

    # Parcourir les données
    for item in data['data']:
        hourly_data = item['hourly']['data']
        for entry in hourly_data:
            try:
                date = entry['date']
                value = entry['value']
            except KeyError:
                continue
            
            dates.append(datetime.fromisoformat(date.replace('Z', '+00:00')))
            valeurs.append(value)

    # Tracer les données
    #plt.figure(figsize=(10, 6))

    plt.plot(dates, valeurs, marker='o', markersize=2, linestyle='-')
    plt.title('Concentration H2S ppb, Pte Faula maison')
    plt.xlabel('Date')
    plt.ylabel('Valeurs (ppb)')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    
    
def avg(data):
    dates = []
    valeurs = []

    # Parcourir les données
    for item in data['data']:
        hourly_data = item['hourly']['data']
        for entry in hourly_data:
            try:
                date = entry['date']
                value = entry['value']
            except KeyError:
                continue
            
            dates.append(datetime.fromisoformat(date.replace('Z', '+00:00')))
            valeurs.append(value)
    return sum(valeurs) / len(valeurs)


def tracer_valeurs_jour_nuit(data):
    """
    Trace une courbe unique des valeurs avec des segments en vert pour le jour (6h-18h)
    et en orange pour la nuit (18h-6h). Calcule et affiche la moyenne des concentrations 
    pour les périodes de jour et de nuit.

    :param data: Dictionnaire contenant les données à tracer.
    """
    # Initialiser les listes pour les dates et les valeurs
    dates = []
    valeurs = []
    
    # Variables pour le calcul des moyennes
    valeurs_jour = []
    valeurs_nuit = []

    # Parcourir les données
    for item in data['data']:
        hourly_data = item['hourly']['data']
        for entry in hourly_data:
            try:
                date = entry['date']
                value = entry['value']
            except KeyError:
                continue
            
            datetime_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
            dates.append(datetime_obj)
            valeurs.append(value)
            
            # Stocker les valeurs dans jour ou nuit
            if 6 <= datetime_obj.hour < 18:
                valeurs_jour.append(value)
            else:
                valeurs_nuit.append(value)

    # Calculer les moyennes
    moyenne_jour = sum(valeurs_jour) / len(valeurs_jour) if valeurs_jour else 0
    moyenne_nuit = sum(valeurs_nuit) / len(valeurs_nuit) if valeurs_nuit else 0

    # Afficher les moyennes
    print(f"Moyenne des concentrations pendant le jour (6h-18h) : {moyenne_jour:.2f} ppb")
    print(f"Moyenne des concentrations pendant la nuit (18h-6h) : {moyenne_nuit:.2f} ppb")

    # Tracer les données avec des segments colorés pour jour et nuit
    plt.figure(figsize=(10, 6))
    
    for i in range(1, len(dates)):
        # Choisir la couleur en fonction de l'heure de début du segment
        color = 'green' if 6 <= dates[i-1].hour < 18 else 'orange'
        
        # Tracer chaque segment individuellement
        plt.plot(dates[i-1:i+1], valeurs[i-1:i+1], color=color, marker='o', markersize=2, linestyle='-')

    plt.title('Concentration H2S ppb, Pte Faula maison')
    plt.xlabel('Date')
    plt.ylabel('Valeurs (ppb)')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()
        