![Icône de l'application](./app/assets/favicon.ico)

## Présentation

L'application permet de planifier un itinéraire à pied ou en transports en commun depuis un point de départ vers un point de départ / d'arrivée de randonnée, ou vers un emplacement ponctuel. 

Elle permet aussi de planifier sa propre randonnée avec des points de passage.

L'élevation est calculée le long des itinéraires à pied.

Un outil d'export permet enfin d'exporter sa randonnée au format GPX, complétées avec les itinéraires de marche pour se rendre au point de départ de la randonnée depuis l'arrêt de bus trouvé (et pareil pour le retour).

Les instructions pour prendre les transports en commun sont copiables et les itinéraires peuvent être exportés au format GPX.

Note : l'application repose sur le téléchargement et l'installation de fichiers divers (rasters, données d'horaires etc). Le fonctionnement est expliqué plus bas.

## Architecture

L'application est constituée de 4 micro-services :
- app : application Dash principale
- alti : application de calcul d'élevation. Utilise des fichiers rasters de la base IGN.
- otp : Open Trip Planner, calcul d'itinéraires en multi-modalité. Utilise des fichiers PBF (données vectorielles de la base OSM) et des fichiers GTFS (données des lignes de transport des opérateurs de mobilité).
- valhalla : calcul d'itinéraires de randonnée. Utilise des fichiers PBF.

## Installation

- Télécharger les fichiers (voir ci-dessous)
- Un docker compose permet de démarrer tous les services à la fois. Lancer la commande `docker-compose up -d`. L'application est visible à l'adresse `http://localhost:8050`.

## Source et fichiers à télécharger 

- Le script `setup.py` permet de télécharger les différents fichiers souhaités (PBF et GTFS) et les place au bon endroit. Il nécessite un fichier de configuration `config.json` répertoriant les URL des fichiers (voir le fichier exemple fourni pour l'Isère).
- Les archives pour l'altimétrie sont à télécharger soi-même. Données Alti IGN : (utiliser 25m ou 5m) https://geoservices.ign.fr/rgealti / https://geoservices.ign.fr/bdalti, et à placer dans l'application `alti` (voir documentation du dossier).
- Extracts d'OSM, à utiliser pour valhalla et otp : https://download.openstreetmap.fr/extracts/europe/france/rhone_alpes/
- Données GTFS pour la planification des itinéraires : https://transport.data.gouv.fr ou https://www.itinisere.fr/fr/donnees-open-data/169/OpenData/Index ou https://data.metropolegrenoble.fr/ckan/dataset/horaires-theoriques-du-reseau-tag
