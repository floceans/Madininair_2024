import matplotlib.pyplot as plt

# Données extraites
import matplotlib.pyplot as plt

# Données
heures = [k for k in range(1, 51)]

concentration_dostaly = [
    0.006, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005,
    0.004, 0.004, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.006,
    0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.006, 0.005, 0.005, 0.004,
    0.005, 0.005, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.005,
    0.005, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.005
]

concentration_preskil = [
    0.092, 0.073, 0.063, 0.083, 0.057, 0.225, 0.225, 0.091, 0.147, 0.133,
    0.068, 0.035, 0.061, 0.113, 0.076, 0.028, 0.034, 0.083, 0.162, 0.047,
    0.078, 0.044, 0.103, 0.175, 0.526, 0.022, 0.14, 0.221, 0.023, 0.028,
    0.122, 0.193, 0.118, 0.022, 0.287, 0.075, 0.119, 0.223, 0.233, 0.194,
    0.278, 0.378, 0.324, 0.302, 0.212, 0.475, 0.355, 0.087, 0.523
]

concentration_fregate = [
    1.331, 1.576, 1.335, 1.652, 0.845, 1.28, 0.793, 0.17, 0.197, 0.37, 0.06, 0, 0.011, 0.228, 
    0.112, 0.004, 0, 0.038, 0.19, 0.095, 0.042, 0.069, 0.139, 0.588, 2.119, 0, 0.033, 0, 0, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0.001, 0.001, 0, 0, 0.018, 0.028
]

# Créer une figure avec trois sous-graphiques
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Tracer les concentrations pour chaque substance
ax1.plot(heures[:len(concentration_dostaly)], concentration_dostaly, marker='o', color='blue')
ax1.set_title('Concentration Dostaly')
ax1.set_ylabel('Concentration')

ax2.plot(heures[:len(concentration_preskil)], concentration_preskil, marker='o', color='green')
ax2.set_title('Concentration Preskil')
ax2.set_ylabel('Concentration')

ax3.plot(heures[:len(concentration_fregate)], concentration_fregate, marker='o', color='red')
ax3.set_title('Concentration Fregate')
ax3.set_xlabel('Heure')
ax3.set_ylabel('Concentration')

# Ajuster l'espacement entre les sous-graphiques
plt.tight_layout()

# Afficher le graphique
plt.show()
