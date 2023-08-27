import os
import geopandas as gpd
import pyproj
import rioxarray as xr
from shapely.geometry import Point
import traceback
import os

path_specs = os.getenv("BD_ALTI_PATH_SPECS")
path_dalles = os.getenv("BD_ALTI_PATH_DALLES")

def get_alti_from_lonlat(points: list[tuple[float, float]]) -> list[int]:
    '''
    From a list of (lon, lat) points, return list of altitudes
    '''
    try:
        
        file = "dalles.shp"
        #Système de coordonnée d'origine
        crs1 = "WGS84"

        #Ouverture du shapefile avec geopandas
        gdf = gpd.read_file(os.path.join(path_specs, file))

        #Système de coordonnées cible (extrait directement du geodataframe)
        crs2 = pyproj.CRS(gdf.crs)

        transformer = pyproj.Transformer.from_crs(crs1, crs2, always_xy=True)
  
        # On va grouper les points par dalle à ouvrir afin de minimiser le temps d'ouverture des fichiers 
        # raster puis on regroupera les altitudes dans le bon ordre 
        points_to_index = {(p[1],p[0]): i for i,p in enumerate(points)}

        dalle_points = {}
        res = [None]*len(points)

        for p in points:
            lat = p[1]
            lon = p[0]
        #WGS84 --> Coordonnées (Lambert93) du point recherché
            x, y = transformer.transform(lon, lat)
            point = Point(x, y)
            #Nom de la dalle à ouvrir
            nom_dalle = gdf[gdf.geometry.contains(point)].iloc[0].NOM_DALLE
            nom_dalle += ".asc"

            # Regroupe tous les points communs à la dalle
            if nom_dalle not in dalle_points.keys():
                dalle_points[nom_dalle] = []
            dalle_points[nom_dalle].append({'wgs': (lat, lon), 'lambert': (x, y)})
        
        for dalle, ps in dalle_points.items():
            # Ouvre la dalle et extrait l'altitude du point puis le remet dans la bonne position
            DS = xr.open_rasterio(os.path.join(path_dalles, dalle))
            for point in ps:
                x,y = point['lambert']
                alt = int(DS.sel(x = x, y = y, method = 'nearest'))
                res[points_to_index[point['wgs']]] = int(alt)

        cluster = none_clusters(res)
        corrected = fill_none(res, cluster)
        return corrected
    except:
        traceback.print_exc()
        return [0]*len(points)

def none_clusters(array: list[int]) -> dict:
    '''
    Extract {start_index: length} of clusters of None in an array
    '''
    clusters = {}
    clustering = False
    current_index = -1
    length = 0
    for i,e in enumerate(array):
        if e is not None:
            if clustering:
                clusters[current_index] = length 
            clustering = False
            length = 0
            continue
        elif not clustering:
            clustering = True
            current_index = i
        length += 1
    if clustering:
        clusters[current_index] = length
    return clusters

def fill_none(array: list[int], clusters: dict) -> list[int]:
    '''
    Fill None items of an array with an interpolation
    '''
    corrected = array
    for i, l in clusters.items():
        if len(array) == l:
            return 'Aucune altitude n\'a pu être calculée.'
        if i == 0:
            corrected[i:i+l] = [array[i+l+1]]*l
        else:
            if i+l+1 >= len(array):
                corrected[i:i+l] = array[i-1]
            else:
                delta = array[i+l+1] - array[i-1]
                for j in range(i, i+l):
                    corrected[j] = int(corrected[j-1] + delta/l)
    return corrected