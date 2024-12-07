import requests
from fun import get_poke_info


pika_info = get_poke_info('pikachu')


class Pokemon :
    def __init__(self, name : str):
        self.name = name
        self.height = get_poke_info(name)['height']
        self.weight = get_poke_info(name)['weight']
        self.base_experience = get_poke_info(name)['base_experience']
    
    def get_name(self):
        return self.name
    
    def get_height(self):
        return self.height
    
    def get_weight(self):
        return self.weight
    
    def get_base_experience(self):
        return self.base_experience
    
    def get_info(self):
        return self.info

pikachu = Pokemon('pikachu')
print(pikachu.get_name())