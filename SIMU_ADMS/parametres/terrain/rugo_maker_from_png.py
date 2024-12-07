from math import *
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from colorama import Fore, Back, Style, init
import PIL as pil
from fun_rug import *
from scipy.ndimage import uniform_filter

file_path_ruf = r'C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\terrain\CODE_PROPRE\concat\francois_sud\dostaly.png'

# Lire les données et les stocker dans une liste de listes #
ruf = pil.Image.open(file_path_ruf)

#png to list of list
ruf = np.array(ruf)
ruf = ruf.tolist()

rugo = rugo_maker(ruf)

# afficher ruf
#show_matrix(ruf)
show_matrix(rugo)

rugo = smooth_matrix(rugo, 10)

# plot rugo
plt.imshow(rugo, cmap='viridis')
plt.colorbar()
plt.show()

