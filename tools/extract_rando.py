import json
from pathlib import Path
from ipyleaflet import Map, Polyline, GeoJSON, Marker
from tqdm.auto import tqdm
import requests
import gpxpy
import visvalingamwyatt as vw
import copy
import numpy as np
from bs4 import BeautifulSoup
import re
import pyproj
import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--output', type=str, help='Output of file')
parser.add_argument('--use-json', action=argparse.BooleanOptionalAction, help="--use-json for saved json data. Otherwise --no-use-json for reloading data from camptocamp.")

args = parser.parse_args()

output = args.output
use_json = args.use_json

path = "."

if not use_json:

    print("Extracting data from HTML files")

    files = list(Path(path).rglob('*.htm'))

    for file in files:
        data = []
        print("File :", file)
        with open(file, "r", encoding="UTF-8") as f:
            bs = BeautifulSoup(f.read(), features="html.parser")
        routes = bs.find_all('a', href=re.compile(r"/routes/\d+"))

        for route in tqdm(routes):
            r = requests.get("https://api.camptocamp.org/routes/" + route["href"].split("/")[-1])
            doc = json.loads(r.content)
            r = requests.get(f"https://api.camptocamp.org/document/{route['href'].split('/')[-1]}/history/fr")
            hist = json.loads(r.content)
            data.append(
                {
                    "document": doc,
                    "versions": hist
                }
            )
        
        with open(file.name + ".json", "w") as f:
            json.dump(data, f)

source_crs = 'epsg:3857' # Coordinate system of the file
target_crs = 'epsg:4326' # Global lat-lon coordinate system
converter = pyproj.Transformer.from_crs(source_crs, target_crs)

routes = []
ids = set()

print("Extracting data from JSON files")

print("Gathering hiking data")

files = list(Path(path).rglob('*.json'))

for file in files:
    print("File :", file)
    with open(file, "r") as f:
        data = json.load(f)


    for page in tqdm(data):
        d = page["document"]
        h = page["versions"]

        if d["document_id"] in ids:
            continue

        act = d["activities"]
        if "hiking" not in act:
            continue

        if "geom_detail" not in d["geometry"].keys() or d["geometry"]["geom_detail"] is None:
            feature = d["geometry"]["geom"]
        else:   
            feature = d["geometry"]["geom_detail"]
        if feature is None:
            continue

        geo = json.loads(feature)
        loc = [l for l in d["locales"] if l["lang"] == "fr"][0]
        title = []
        if loc["title_prefix"]:
            title.append(loc["title_prefix"])
        if loc["title"]:
            title.append(loc["title"])
        name = " - ".join(title)
        coordinates = geo["coordinates"]
        type_ = geo["type"]
        final = []
        
        if type_ == "Point":
            final = list(converter.transform(coordinates[0], coordinates[1]))
        else:
            for c in coordinates:
                if type_ == "LineString":
                    final.append(list(converter.transform(c[0], c[1])))
                
                else: #MultiLineString
                    for coord in c:
                        final.append(list(converter.transform(coord[0], coord[1])))

        author = h["versions"][0]["name"]
        areas = ', '.join([l["title"] for a in d["areas"] for l in a["locales"] if l["lang"] == "fr"])

        routes.append({
            "id": d["document_id"],
            "name": name,
            "rating": d["hiking_rating"],
            "coordinates": final,
            "type": "Point" if type_ == "Point" else "LineString",
            "author": author,
            "areas": areas
        })
        ids.add(d["document_id"])

print("Generating CSV file, output is", output)

pd.DataFrame(routes).to_csv(output, index=False)