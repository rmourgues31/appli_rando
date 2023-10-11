## OTP

Service utilisant l'image Docker d'OTP https://hub.docker.com/r/opentripplanner/opentripplanner

#### Installation

- Ligne de commande pour construire le graphe et le sauver :   
`docker run --rm -v "$PWD/opentripplanner:/var/opentripplanner" opentripplanner/opentripplanner:2.3.0 --build --save`

#### Documentation

- Documentation: https://docs.opentripplanner.org/en/v2.3.0/Basic-Tutorial/ 
- GitHub: https://github.com/opentripplanner/OpenTripPlanner
