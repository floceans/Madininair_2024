from math import *
from numpy import *
from scipy import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from tqdm import tqdm
from colorama import Fore, Back, Style


def rmse_ploter(dict_zone):
    mesures = extraire_mesures(dict_zone)
    concentrations_adms = extraire_concentrations(dict_zone)
    facteur_emission = extraire_facteurs_emission(dict_zone)[0]
    rmse_values = []
    print("mesures : ",mesures)
    print("concentrations ADMS : ",concentrations_adms)
    print("facteurs d'émission : ",facteur_emission)
    
    for k in range (len(concentrations_adms[0])):
        conc = [concentrations_adms[i][k] for i in range (len(concentrations_adms))]
        print("conc : ",conc)
        print("mesures : ",mesures)
        rmse_values.append(rmse(conc, mesures))
    
    print("RMSE : ",rmse_values)
    
    # ADIM


    rmse_values = moyenne_courbe(rmse_values)

    plt.loglog(facteur_emission, rmse_values, marker='o', linestyle='-', markersize=3) #, color='b')
    plt.xlabel('Facteur d\'émission (g.m⁻².s⁻¹)')
    plt.ylabel('RMSE adimensionnel')
    plt.title('RMSE en fonction du facteur d\'émission, data [08-09/2024]')
    
    return facteur_emission[indice_min(rmse_values)]


    
def indice_min(liste):
    min = liste[0]
    indice = 0
    for k in range (len(liste)):
        if liste[k] < min:
            min = liste[k]
            indice = k
    return indice


def extraire_concentrations(zone_fregate):
    concentrations = []
    for site_key in zone_fregate:
        if isinstance(zone_fregate[site_key], dict):  # Vérifier que c'est bien un site
            site_data = zone_fregate[site_key]
            site_concentrations = [adms[1] for adms in site_data['ADMS']]  # Extraire les concentrations
            concentrations.append(site_concentrations)
    
    return concentrations

def adim_buider(FACTEURS_EMISS, DIST_SOURCE, SURF_SOURCE):
    adim = []

    for k in range (len(FACTEURS_EMISS)):
        adim.append(DIST_SOURCE[k]/SURF_SOURCE[k]**2)
    return adim

def rmse(calc, mesures):
    if len(calc) != len(mesures):
        raise ValueError("Les listes 'calc' et 'mesures' doivent avoir la même longueur.")
    somme_carre_diff = sum((c - m) ** 2 for c, m in zip(calc, mesures))
    mean_carre_diff = somme_carre_diff / len(calc)
    return sqrt(mean_carre_diff)

def extraire_mesures(zone_fregate):
    mesures = []
    
    # Parcourir les sites dans zone_fregate
    for site_key in zone_fregate:
        if isinstance(zone_fregate[site_key], dict):  # Vérifier que c'est bien un site
            site_data = zone_fregate[site_key]
            mesures.append(site_data['mesure'])  # Extraire la valeur de 'mesure'
    
    return mesures


def extraire_facteurs_emission(zone_fregate):
    facteurs_emission = []
    
    # Parcourir les sites dans zone_fregate
    for site_key in zone_fregate:
        if isinstance(zone_fregate[site_key], dict):  # Vérifier que c'est bien un site
            site_data = zone_fregate[site_key]
            site_facteurs_emission = [adms[0] for adms in site_data['ADMS']]  # Extraire les facteurs d'émission
            facteurs_emission.append(site_facteurs_emission)
    
    return facteurs_emission

def moyenne_distances(zone):
    # Récupérer les distances
    distances = []
    
    for site_key, site_value in zone.items():
        if site_key.startswith('site_'):
            distance = site_value.get('distance', None)
            if distance is not None:
                distances.append(distance)
    
    # Calculer la moyenne des distances
    if len(distances) > 0:
        moyenne = sum(distances) / len(distances)
    else:
        moyenne = None  # Si aucune distance n'est trouvée
    
    return moyenne

def moyenne_courbe(L):
    moyenne = 0
    for k in range (len(L)):
        moyenne += L[k]
    for k in range (len(L)):
        L[k] = L[k]/moyenne
    return L


zone_thalemont = {
    'surface': 680,
    'site_1' : {
        'nom': 'Pointe Thalémont',
        'latitude': 14.6434,
        'longitude': -60.8987,
        'distance': 40,
        'mesure': 0.7283, #0.6315, # 0.178, # 188 mesures
        'mesure_jour' : 0,
        'mesure_nuit' : 0,
        'ADMS': [[5e-3, 4.194], [1.5e-3,1.260], [1e-3, 0.8390], [8.5e-4, 0.7129], [8e-4, 0.6710], [7.5e-4, 0.629],[6.9e-4, 0.5787], [6.25e-4, 0.5242], [5e-4, 0.4194], [2.5e-4, 0.2097], [1.5e-4, 0.126]]
    }
}



zone_fregate = {
    'surface': 5500,
    'site_1' : {
        'nom': 'fregate_bord_mer',
        'latitude': 14.6082,
        'longitude': -60.8755,
        'distance': 30,
        'mesure': 0.447,
        'mesure_jour' : 0.488,
        'mesure_nuit' : 0.637,
        'ADMS': [[5e-3, 15.527], [1e-3, 3.105],[5e-4, 1.553], [2.5e-4, 0.77], [2e-4, 0.6211], [1.5e-4, 0.466], [1.25e-4, 0.3882], 
                 [1e-4, 0.31], [7.5e-5, 0.233], [5e-5, 0.155], [2e-5, 0.0621], [1e-5, 0.031]] # emission factor, concentration
    },
    'site_2' : {
        'nom': 'fregate_maison_terre',
        'latitude': 14.608691,
        'longitude': -60.876371,
        'distance': 110,
        'mesure': 0.132,
        'mesure_jour' : 0.169,
        'mesure_nuit' : 0.159,
        'ADMS': [[5e-3, 1.139], [1e-3, 0.228],[5e-4, 0.114], [2.5e-4, 0.057], [2e-4, 0.04555], [1.5e-4, 0.0342], [1.25e-4, 0.02847],
                 [1e-4, 0.022], [7.5e-5, 0.0171], [5e-5, 0.0114], [2e-5, 0.00456],[1e-5, 0.0023]] # emission factor, concentration
    }
}


zone_FaC = {
    'surface': 1000,
    'site_1' : {
        'nom': 'Four à Chaux',
        'latitude': 14.660575,
        'longitude': -60.934664,
        'distance': 40,
        'mesure': 0.4625,
        'mesure_jour' : 1.106,
        'mesure_nuit' : 0.908,
        'ADMS': [[2e-5, 0.014873], [5e-5, 0.03718], [1e-4, 0.07436], [1.25e-4, 0.09296], [1.5e-4, 0.11155], [1.75e-4, 0.13014], [2e-4, 0.14873], 
                 [2.5e-4, 0.18591], [3e-4, 0.2231], [3.5e-4, 0.26028], [4.25e-4, 0.31605], [5e-4, 0.3893], [5.8e-4, 0.43132], [6.25e-4, 0.4648],  
                 [7e-4, 0.52055], [7.5e-4, 0.5577], [1.5e-3, 1.1155], [5e-3, 3.7183]] # emission factor, concentration
    }
}

zones_pontalery = {
    'surface': 500,
    'site_1' : {
        'nom': 'Pontaléry',
        'latitude': 14.670525,
        'longitude': -60.943135,
        'distance': 25,
        'mesure': 0.04,
        'mesure_jour' : 0.347,
        'mesure_nuit' : 0.388,
        'ADMS': [[2e-5, 0.0048258], [5e-5, 0.01206], [1e-4, 0.02413], [1.25e-4, 0.030162], [1.5e-4, 0.03619], [1.75e-4, 0.042226], [2e-4, 0.0482583], 
                 [2.5e-4, 0.060323], [3e-4, 0.0723875], [3.5e-4, 0.08445], [4.25e-4, 0.10255], [5e-4, 0.12], [5.8e-4, 0.1399], [6.25e-4, 0.1508], 
                 [7e-4, 0.1689], [7.5e-4, 0.1810], [1.5e-3, 0.3619], [5e-3, 1.20646]] # emission factor, concentration
    }
}

zones_pte_faula = {
    'surface': 1000,
    'site_1' : {
        'nom': 'Faula club nautique',
        'latitude': 14.542511,
        'longitude': -60.830209,
        'distance': 15,
        'mesure': 0.023, #0.0185, #0.8433,
        'mesure_jour' : 0,
        'mesure_nuit' : 0,
        'ADMS': [[1e-5, 0.00173], [5e-5, 0.00566], [7.5e-5, 0.006465], [1e-4, 0.0173], [1.5e-4, 0.02599], [2e-4, 0.0365], [2.5e-4, 0.0433], [5e-4, 0.0867], [1e-3, 0.173], [5e-3, 0.867]] #[[1e-4, 0.01999], [5e-4, 0.09996], [7.5e-4, 0.1499]] # juste avec src ppal
    },
    'site_2' : {
        'nom': 'Faula Miguel',
        'latitude': 14.54111,
        'longitude': -60.83041,
        'distance': 100,
        'mesure': 0.0053,
        'mesure_jour' : 0,
        'mesure_nuit' : 0,
        'ADMS': [[1e-5, 0.0000689], [5e-5, 0.0003447], [7.5e-5, 0.00053], [1e-4, 0.000689], [1.5e-4, 0.001034],  [2e-4, 0.001379], [2.5e-4, 0.00172], [5e-4, 0.00345], [1e-3, 0.00689], [5e-3, 0.0345]]
    }
}




print("\n")

noms_sites =  ['Pte Faula', 'Four à Chaux', 'Pontaléry', 'Pointe Thalémont', 'Frégate']

"""
concentrations = [[0.365, 0.5], [0.228, 0.5]]
mesures = [0.447, 0.132]
facteur_emission = [[10e-3, 10e-1], [10e-3, 10e-1]]
"""

facteurs_opti = []

facteurs_opti.append(rmse_ploter(zones_pte_faula))
facteurs_opti.append(rmse_ploter(zone_FaC))
facteurs_opti.append(rmse_ploter(zones_pontalery))
facteurs_opti.append(rmse_ploter(zone_thalemont))
facteurs_opti.append(rmse_ploter(zone_fregate))

'''
rmse_ploter(zone_FaC)
rmse_ploter(zones_pontalery)
rmse_ploter(zone_thalemont)
rmse_ploter(zone_fregate)
'''

plt.legend(noms_sites)
plt.show()

d = []

d.append(moyenne_distances(zones_pte_faula)**2 / zones_pte_faula['surface'])
d.append(moyenne_distances(zone_FaC)**2 / zone_FaC['surface'])
d.append(moyenne_distances(zones_pontalery)**2 / zones_pontalery['surface'])
d.append(moyenne_distances(zone_thalemont)**2 / zone_thalemont['surface'])
d.append(moyenne_distances(zone_fregate)**2 / zone_fregate['surface'])

couleurs = ['y', 'b', 'g', 'r', 'c']


for i in range(len(d)):
    plt.scatter(d[i], facteurs_opti[i], color=couleurs[i], label=noms_sites[i])

# Ajout des légendes et labels
plt.xlabel('\u03B4 = Distance²/Surface')
plt.ylabel('Facteurs d\'émission calculés (g/m²/s)')
plt.title('Distribution des Facteurs d\'émission en fonction de \u03B4')
plt.legend()
plt.show()

