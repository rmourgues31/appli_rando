## OTP

#### Installation

- Mettre les archive GTFS.ZIP dans le répertoire opentripplanner
- Mettre les données OSM.PBF dans le répertoire opentripplanner  
ex: `curl -L https://download.openstreetmap.fr/extracts/europe/france/rhone_alpes/isere-latest.osm.pbf -o opentripplanner/isere-latest.osm.pbf`
- Ligne de commande :   
`docker run --rm -v "$PWD/opentripplanner:/var/opentripplanner" opentripplanner/opentripplanner:2.3.0 --build --save` pour construire le graphe et le sauver

#### Documentation

- Documentation: https://docs.opentripplanner.org/en/v2.3.0/Basic-Tutorial/ 
- GitHub: https://github.com/opentripplanner/OpenTripPlanner
