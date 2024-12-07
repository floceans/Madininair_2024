# Paramètres de connexion à XR
URL_XR_V1 = "https://172.16.49.33:8443/dms-api/public/v1"
URL_XR_V2 = "https://172.16.49.33:8443/dms-api/public/v2"

# Paramètre logique
ENVOI_INITIAL = False
ANNEE_ENVOI_INITIAL = "2020"

def print_dico(dico):
    for key, value in dico.items():
        print(key, ":", value)
        if type(value) == dict:
            print_dico(value)
        print("\n")