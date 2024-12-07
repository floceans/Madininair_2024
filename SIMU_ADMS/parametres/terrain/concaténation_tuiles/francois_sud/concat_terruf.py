def concat_files(file1, file2, output_file):
    # Initialiser un compteur de ligne
    line_number = 1
    
    # Ouvrir le fichier de sortie en mode écriture
    with open(output_file, 'w') as output:
        # Concaténer le contenu du premier fichier
        with open(file1, 'r') as f1:
            for line in f1:
                # Split la ligne en ses composants
                parts = line.strip().split(',')
                
                # Remplacer le premier élément (numéro de ligne) par la nouvelle valeur
                parts[0] = str(line_number)
                
                # Recréer la ligne avec le bon numéro et écrire dans le fichier de sortie
                output.write(','.join(parts) + '\n')
                
                # Incrémenter le compteur de ligne
                line_number += 1
        
        # Concaténer le contenu du deuxième fichier
        with open(file2, 'r') as f2:
            for line in f2:
                # Split la ligne en ses composants
                parts = line.strip().split(',')
                
                # Remplacer le premier élément (numéro de ligne) par la nouvelle valeur
                parts[0] = str(line_number)
                
                # Recréer la ligne avec le bon numéro et écrire dans le fichier de sortie
                output.write(','.join(parts) + '\n')
                
                # Incrémenter le compteur de ligne
                line_number += 1

    print(f"Le fichier {output_file} a été créé avec succès en concaténant {file1} et {file2} avec des numéros de ligne corrects.")

# Exemple d'utilisation



file_2 = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\terrain\CODE_PROPRE\concat\francois_sud\dostalax.ruf"
file_1 = r"C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\terrain\CODE_PROPRE\concat\francois_sud\fregate_oui.ruf"

# Exemple d'utilisation
concat_files(file_1, file_2, r"C:\Users\service.si\OneDrive - MADININAIR\Documents\Simu_ADMS\terrain\fichiers ter & ruf\francois_sud_2.ruf")
