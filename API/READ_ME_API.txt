READ_ME API

Nécessité d'être connecté sur réseau local Madininair
Requètes allant chercher sur serveur local données de concentration en polluants captées par différents dispositifs sur site
Capteur équipé de carte SIM envoie automatiquement en direct au serveur ses données

Formation url requette avec comme paramètres :
- capteur & polluant (se référer à Power BI pour noms) (ex : cairnet_48 = ['H2S-CH4S_073_Q_'])
- début période
- fin période
- moyennage des données (horaire, journalier, brut...)

affiche concentrations correspondant à requette et enregistre dans un json

main_api.py réuni les appels, seul script à exécuter

