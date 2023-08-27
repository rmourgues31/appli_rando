
from pathlib import Path
import zipfile
import pandas as pd
from string import Template
import json

'''
Build a config file for the script gtfs-to-geojson.
Read all GTFS files from OTP folder, gather all agencies and build the config file based on template.
'''

path = "../otp"
files = list(Path(path).rglob('*.GTFS.zip'))

ids = []

for file in files:
    archive = zipfile.ZipFile(file, 'r')
    agencies = pd.read_csv(archive.open('agency.txt'))
    for row in agencies.itertuples():
        ids.append({
            "agency_key": row.agency_id,
            "path": str(file),
            "agency_name": row.agency_name
        })

d = {
    'agencies': json.dumps(ids, ensure_ascii=False)
}

with open('gtfs_geojson_template.json', 'r') as template:
    src = Template(template.read())
    result = src.substitute(d)

with open('config.json', "w", encoding="UTF8") as f:
    f.write(result)
