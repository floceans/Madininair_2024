import requests

base_url = r'https://pokeapi.co/api/v2/pokemon/'
 
def get_poke_info(name : str) -> dict:
    request_url = base_url + name
    reponse = requests.get(request_url)
    
    if requests.get(request_url).status_code == 200:
        print('>> Data found <<')
        return reponse.json()
    else:
        return "Poké-error numéro " + str(requests.get(request_url).status_code)