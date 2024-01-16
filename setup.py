import json
import urllib.request
import shutil
import argparse
import zipfile
import traceback
import os

parser = argparse.ArgumentParser()

parser.add_argument('--gtfs', action=argparse.BooleanOptionalAction, help='--gtfs to download GTFS files. Otherwise --no-gtfs.')
parser.add_argument('--pbf', action=argparse.BooleanOptionalAction, help='--pbf to download PBF files. Otherwise --no-pbf.')

args = parser.parse_args()

use_gtfs = args.gtfs
use_pbf = args.pbf

with open("config.json", "r") as f:
    config = json.load(f)
    
print("Download GTFS files:", use_gtfs)

if use_gtfs:
    gtfs = config["gtfs"]

    print(len(gtfs), " GTFS files to download.")

    for [url, name] in gtfs:
        print("File:", name)
        try:
            path = f"./otp/opentripplanner/{name}"
            urllib.request.urlretrieve(url, path)
            
            archive = zipfile.ZipFile(path, 'r')
            if "agency.txt" not in archive.namelist():
                archive.extractall(path+"2")
                os.remove(path)
                dest = zipfile.ZipFile(path, "w+")
                for file in archive.namelist():
                    dest.write(path+"2/"+file, arcname=file)
                shutil.rmtree(path+"2")
                
        except Exception as e:
            traceback.print_exc()

print("Download PBF files:", use_pbf)

if use_pbf:
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