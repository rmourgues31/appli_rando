## App principale

#### Installation

Pour Valhalla :
- Si ACTOR est renseigné dans les variables d'environnement, l'application utilisera le binder avec les fichiers locaux. Ne marche pas avec Docker !
- Sinon renseigner une autre valeur pour lancer le serveur.

Pour l'app :
- Installer les librairies par ex avec `pipenv install`. Installer aussi `gunicorn` si ce n'est pas fait.
- Lancer l'application avec `pipenv run python .\index.py`

#### Documentation

- https://dash-leaflet.herokuapp.com/#components

Pour Valhalla :
- https://github.com/gis-ops/docker-valhalla
- https://hub.docker.com/r/gisops/valhalla 
- https://gis-ops.com/valhalla-how-to-run-with-docker-on-ubuntu/
- https://github.com/valhalla/valhalla
- https://valhalla.github.io/valhalla/api/
- https://github.com/gis-ops/valhalla-app/