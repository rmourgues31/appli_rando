## Geojson tools

Pour visualiser les arrêts de bus sur la carte :
- Installer `gtfs-to-geojson` https://github.com/BlinkTagInc/gtfs-to-geojson 
- Faire tourner le script `build_gtfs_geojson_config.py` dans `geojson_tools`
- Faire tourner le script `geojson_tooltip.py`
- Dans les assets, un dossier geojson regroupe les arrêts des différents opérateurs au format geojson, à copier dans les assets de l'app principale.

Dans une version ultérieure, les tracés des lignes seront ajoutés à partir des données des opérateurs disponibles sur le portail https://transport.data.gouv.fr.

## Extract rando

Programme python servant à extraire des itinéraires depuis des articles de camptocamp au format HTML (nécessite d'avoir le fichier HTML complet).