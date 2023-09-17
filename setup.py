import json
import urllib.request
import shutil

with open("config.json", "r") as f:
    config = json.load(f)

gtfs = config["gtfs"]

print(len(gtfs), " GTFS files to download.")

for [url, name] in gtfs:
    print("File:", name)
    try:
        urllib.request.urlretrieve(url, f"./otp/opentripplanner/{name}")
    except Exception as e:
        print(e)

pbf = config["pbf"]

print(len(pbf), " PBF files to download.")

for pbf_file in pbf:
    print("File:", pbf_file)
    try:
        name = pbf_file.split("/")[-1]
        urllib.request.urlretrieve(pbf_file, f"./otp/opentripplanner/{name}")
        shutil.copyfile(f"./otp/opentripplanner/{name}", f"./valhalla/custom_files/{name}")
    except Exception as e:
        print(e)

print("Finished")