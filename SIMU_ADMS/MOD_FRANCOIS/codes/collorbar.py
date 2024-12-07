import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Définition des couleurs
colors = ["#50f0e6", "#50ccaa", "#f0e641", "#FF5050", "#960032", "#7D2181"]

# Création d'un colormap personnalisé
color_madininair = LinearSegmentedColormap.from_list("custom_cmap", colors)


