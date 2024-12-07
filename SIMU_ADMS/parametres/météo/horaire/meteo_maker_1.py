import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta


'''
VARIABLES:
10
YEAR
TDAY
THOUR
T0C
RHUM
U
PHI
FTHETA0
P
H
'''

def matrix_to_txt(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            line = ','.join(map(str, row))  # Convertir chaque élément de la ligne en chaîne et les joindre par des virgules
            file.write(line + '\n')  # Écrire la ligne dans le fichier et ajouter un saut de ligne


def extract_date_time(date_string):
    
    # Extraire chaque composante en utilisant le découpage de chaîne
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    hour = int(date_string[8:10])

    return year, month, day, hour


def day_of_year(month, day):
    # Créer une date pour l'année actuelle avec le mois et le jour spécifiés
    date = datetime(datetime.now().year, month, day)

    # Extraire le jour de l'année à partir de la date créée
    day_of_year = date.timetuple().tm_yday

    return day_of_year

def convertisseur_jcm2_wm2(jcm2):
    alpha = 100/36
    int(jcm2)
    return jcm2*alpha

def mada_to_greenwitch(annee, jour, heure):
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


M = [[]]

## read csv file into matrix M

path = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\météo\horaire\MET_VAUCLIN_09.csv'

with open(path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        M.append(row)
    M.pop(0)
    

def string_to_list(s):
    # Diviser la chaîne par le point-virgule
    str_list = s.split(';')
    for k in range(len(str_list)):
        if str_list[k] == '':
            str_list[k] = '0'

    # Convertir chaque élément en entier
    int_list = [num for num in str_list]

    return int_list



for k in range (len(M)):
    #bien formater
    M[k] = string_to_list(str(M[k][0]))
    
    
    if k != 0:
        #changer format date M
        year, month, day, hour = extract_date_time(M[k][4])
        day = day_of_year(month, day)
        new_year, new_day, new_hour = mada_to_greenwitch(year, day, hour)
        M[k].pop(4) # date initiale (AAAAMMJJHH)
        if new_hour == 24:
            new_day += 1
            new_hour = 0
        M[k].insert(0, new_year)
        M[k].insert(1, new_day)
        M[k].insert(2, new_hour)
        

        
        M[k].pop(3) # nom lieu
        M[k].pop(3) # latitude
        M[k].pop(3) # longitude
        
        # convertir rayonnement en W/m2
        #M[k][-1]=convertisseur_jcm2_wm2(int(M[k][-1]))

        
        
    if k==0:
        # format temps
        M[k].pop(4)
        M[k].insert(0, 'YEAR')
        M[k].insert(1, 'TDAY')
        M[k].insert(2, 'THOUR')
        
        M[k].pop(3) # nom lieu
        M[k].pop(3) # latitude
        M[k].pop(3) # longitude
        #M[k].append('SOLAR RAD')
        
    M[k].pop(3) # retirer altitude
    #M[k].pop(-2) # retirer minute ensoleillement
    #M[k].pop(6) # retirer vent max

    

# bords date correction
M[1][1]=1
M[2][1]=1
M[3][1]=1
M[4][1]=1   


############ SYNTAXE ##############

P = M[0] #variable intermédiaire


for i in range(len(M[0])): #titre des variables en début de doc
    M.insert(1+i, [P[i]])

M.insert(1, [str(len(P))]) # nombre de variables

M[0]=['VARIABLES:']

M.insert(len(P)+2, ['DATA:'])
            
print('data ligne 50 :', M[52])



matrix_to_txt(M,  r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\météo\horaire\VAUCLIN_SEPTEMBRE.met')


