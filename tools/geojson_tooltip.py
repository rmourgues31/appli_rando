from pathlib import Path
import shutil
import json
import os
from tqdm.auto import tqdm

'''
Read output from gtfs-to-geojson and isolate Points (transit stops).
Build a new GeoJSON with tooltips displaying some interesting data for the map.
'''

def build_tooltip(prop):
    desc = []
    desc.append(prop["stop_name"])
    desc.append("Opérateur : " + prop["agency_name"])
    if len(prop["routes"]) > 0:
        desc.append("Arrêt desservi par :")
        for r in prop["routes"]:
            match r["route_type"]:
                case 0 | 5:
                    mode = "Tram"
                case 1:
                    mode = "Métro"
                case 2:
                    mode = "Train"
                case 3 | 11:
                    mode = "Bus"
                case 4:
                    mode = "Ferry"
                case 6:
                    mode = "Téléphérique"
                case 7: 
                    mode = "Funiculaire"
                case _:
                    mode = "Inconnu"
            desc.append(f'{mode} {r["route_short_name"]} - {r["route_long_name"]}')
        return '<br>'.join(desc)

asset_path = "../app/assets/geojson/"
if os.path.exists(asset_path):
    shutil.rmtree(asset_path)
Path(asset_path).mkdir()

path = "./geojson"
files = list(Path(path).rglob('*.geojson'))

for file in files:
    print("Reading file ", file)
    with open(file, "r", encoding="UTF8") as f:
        r = json.load(f)
        
    if len(r["features"]) == 0:
        continue

    feats = []

    for i, feature in tqdm(enumerate(r["features"])):

        if feature["geometry"]["type"] != "Point":
            continue

        prop = feature["properties"]
        if not "tooltip" in prop.keys():
            prop["tooltip"] = build_tooltip(prop)
            
        feats.append(feature)

    geo = {'type':'FeatureCollection', 'features': feats}

    with open(f"{asset_path}{file.name}", "w", encoding="UTF8") as f:
        json.dump(geo, f, ensure_ascii=False)
