# Carto

## Architecture

L'application est constituée de 4 micro-services :
- app : application Dash principale
- alti : application de calcul d'élevation
- otp : Open Trip Planner, calcul d'itinéraires en multi-modalité
- valhalla : calcul d'itinéraires de randonnée

Un docker compose permet de démarrer tous les services à la fois une fois les fichiers générés.

## Fichiers à télécharger 

- Extracts d'OSM, à utiliser pour valhalla et otp : https://download.openstreetmap.fr/extracts/europe/france/rhone_alpes/
- Données GTFS pour la planification des itinéraires : https://transport.data.gouv.fr ou https://www.itinisere.fr/fr/donnees-open-data/169/OpenData/Index ou https://data.metropolegrenoble.fr/ckan/dataset/horaires-theoriques-du-reseau-tag 
- Données Alti IGN : (utiliser 25m ou 5m) https://geoservices.ign.fr/rgealti


# TODO

- [ ] Avant déploiement
    - [ ] Docker compose : faire attendre que les autres services soient lancés avant de démarrer app
    - [ ] Terminer la doc readme
    - [ ] Nettoyer le dossier
    - [ ] Nouveau repo propre
    - [ ] Se renseigner sur OVH et le nom de domaine
    - [ ] Déplyer sur heroku app ?
- [ ] Design
    - https://github.com/ucg8j/awesome-dash
    - https://dash.gallery/Portal/
    - https://hellodash.pythonanywhere.com/
    - https://dashcheatsheet.pythonanywhere.com/
