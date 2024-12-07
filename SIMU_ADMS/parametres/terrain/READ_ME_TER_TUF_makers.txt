TER_MAKER :

- Télécharger fichier RGE-ALTI sur site IGN
-Ouvrir avec QGIS
-Reprojeter en epsg 3395 (possible sur python mais temps de calcul très long, ~1h pour 25km^2), enregistrer
-Découper selon emprise si nécéssaire, enregistrer
-Exporter en .xyz : Raster/conversion/ enregistrer un fichier .xyz

- Executer script python ter_maker_from_xyz.py, en faisant correspondre le nom du fichier dans le code (variable input_file)

- Le fichier .ter à été créé, prèt à être importer dans ADMS






RUF_MAKER

- Depuis Corine Landcover de copernicus, exporter partir de la carte souhaitée en .png (export ou capture ecran possible)
	ATTENTION : Prendre exactement la même zone que .ter fait précédement
	Coordonées gps dispo dans onglet measurment sur site Copernicus pour précision

- Faire correspondre le nom des fichiers source avec le nom & chemin des fichiers dans le script (source : .ter & .png)
-  Exécuter script python ruf_maker.py
- Le fichier .ruf à été créé