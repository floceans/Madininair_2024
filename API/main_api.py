from XR import *


# cairnet 50 pte faula

xr = Xr()


#afficher_sites(xr.get_sites())


# Définissez les paramètres
data_type = 'hourly'
cairnet_48 = ['H2S-CH4S_073_Q_']  # ID de la mesure H2S maison faula
cairnet_50 = ['H2S-CH4S_075_Q_']  # ID de la mesure H2S faula club nautique
cairnet_6 = ['H2S-CH4S_023_Q_']  # ID de la mesure H2S cairnet 6 pte faula

date_debut = '2024-06-01'
date_fin = '2024-10-28'

# Récupérez les données

data_1 = xr.get_data_from_period(dType=data_type, listeMesures=cairnet_6, dDebut=date_debut, dFin=date_fin)
#data_2 = xr.get_data_from_period(dType=data_type, listeMesures=cairnet_50, dDebut=date_debut, dFin=date_fin)

#data = xr.get_data_from_last_hours(dType='hourly', listeMesures=liste_mesures, nHours=2)

#data = xr.get_data_updated_since(dataTypes=['hourly'], listeMesures=cairnet_48, dateSince='2024-09-15')

tracer_valeurs(data_1)
#tracer_valeurs_jour_nuit(data_2)

plt.show()

print('\n')
print('-' * 130)

#print('> > > Moyenne :', avg(data_2))
print('> > > Moyenne :', avg(data_1))

print('-' * 130)
print('\n')
