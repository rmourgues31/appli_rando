## OTP

#### Installation

- Suivre la documentation d'OTP, télécharger le fichier jar https://repo1.maven.org/maven2/org/opentripplanner/otp/2.3.0/otp-2.3.0-shaded.jar
- Mettre les archive GTFS.ZIP dans le même répertoire que le jar
- Mettre les données OSM.PBF dans le même répertoire que le jar
- Ligne de commande : 
    - `java -Xmx2G -jar otp-2.3.0-shaded.jar --build --serve ./` dans le répertoire OTP pour construire le graphe à chaque démarrage de serveur
    - `java -Xmx2G -jar otp-2.3.0-shaded.jar --build --save .` pour construire le graphe et le sauver (conseillé)
    - `java -Xmx2G -jar otp-2.3.0-shaded.jar --load .` pour démarrer le serveur avec le graphe du disque (conseillé)

#### Documentation

- Documentation: https://docs.opentripplanner.org/en/v2.3.0/Basic-Tutorial/ 
- GitHub: https://github.com/opentripplanner/OpenTripPlanner