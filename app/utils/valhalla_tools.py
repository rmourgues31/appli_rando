from datetime import datetime
import json
import requests
import traceback
import os
from valhalla import Actor, get_config
from valhalla.utils import decode_polyline
from utils.date_time import datetime_from_iso
from utils.geo import reduce_line

use_actor = os.getenv("USE_ACTOR") == "ACTOR"
port = os.getenv("VALHALLA_PORT")
valhalla_url = "http://" + os.getenv("VALHALLA_SERVICE") + ((":" + port) if port else "") 

if use_actor:
    config = get_config(tile_extract=os.getenv("VALHALLA_TILES"), verbose=True)
    # instantiate Actor to load graph and call actions
    actor = Actor(config)

def get_route(points: list[tuple[float, float]], hike_difficulty: int, _datetime: datetime) -> dict:
    '''
    Compute a route between (lat, lon) points
    '''
    body = {
            #"verbose": True, 
            "locations":[{"lat": p[0], "lon": p[1]} for p in points], 
            "costing": "pedestrian",
            "costing_options":{
                "pedestrian":{
                    "alley_factor": 2,
                    "driveway_factor": 5,
                    "exclude_polygons": [
                    ],
                    "max_hiking_difficulty": hike_difficulty,
                    "service_factor": 1,
                    "service_penalty": 15,
                    "shortest": True,
                    "sidewalk_factor": 1,
                    "step_penalty": 0,
                    "transit_start_end_max_distance": 2145,
                    "transit_transfer_max_distance": 800,
                    "use_ferry": 1,
                    "use_hills": 0.5,
                    "use_lit": 0,
                    "use_living_streets": 0.5,
                    "use_tracks": 0,
                    "walking_speed": 5.1,
                    "walkway_factor": 1
                }
            },
            "date_time": _datetime.isoformat(),
            "directions_options": {
                "units": "kilometers"
            },
            "id":"valhalla_directions"
        }
    if use_actor:
        route = actor.route(body)["trip"]
    else:
        r = requests.get(valhalla_url + '/route', 
                        params={'json': json.dumps(body,separators=(",", ":"))})
        if r.status_code != 200:
            return {}
        c = json.loads(r.content)
        route = c['trip']

    summary = route["summary"]
    itinerary = {
        "distance": summary["length"],
        "temps": summary["time"],
        "segments": []
    }
    segments = []
    for leg in route['legs']:
        coords = decode_polyline(leg['shape'])
        for m in leg['maneuvers']:
            if m["length"] == 0:
                continue
            seg = {
                "mode": m["travel_mode"],
                "geometrie": [(c[1], c[0]) for c in coords[m["begin_shape_index"]:m["end_shape_index"]]],
                "distance": m["length"], # meters
                "temps": m["time"]
            }
            if m["travel_mode"] == "transit":
                info = m["transit_info"]
                transit = {
                    "type": m["travel_type"],
                    "short_name": info["short_name"],
                    "long_name": info["long_name"],
                    "arret_depart": info["transit_stops"][0]["name"],
                    "arret_arrivee": info["transit_stops"][-1]["name"],
                    "heure_depart": datetime_from_iso(info["transit_stops"][0]["departure_date_time"]),
                    "heure_arrivee": datetime_from_iso(info["transit_stops"][-1]["arrival_date_time"]),
                    "couleur": info["color"],
                    "operateur": info["operator_name"],
                    "operateur_url": info["operator_url"]
                }
                seg["transit"] = transit
            segments.append(seg)
    itinerary["segments"] = fuse_walk_segments(segments)
    return {0: itinerary}

def fuse_walk_segments(segments: list[dict]) -> list[dict]:
    '''
    Given a list of segments, fuse walkable ones in an unique item
    '''
    segs = []
    current = False
    current_seg = {}
    for seg in segments:
        if seg["mode"] == "pedestrian":
            if not current:
                current = True
                current_seg = seg
            else:
                for key in ["distance", "temps", "geometrie"]:
                    current_seg[key] += seg[key]
        else:
            if current:
                current = False
                segs.append(current_seg)
            segs.append(seg)
    if current:
        segs.append(current_seg)
    return segs

def get_walk_from_markers(points: list[tuple[float, float]], hike_difficulty: int) -> list[tuple[float]]:
    '''
    Return an unique list of coordinates that goes through 2 markers with (lat, lon) coordinates
    '''
    r = get_route(points, hike_difficulty, datetime.today().replace(second=0, microsecond=0))
    if len(r) == 0:
        return []
    all_coords = [segment["geometrie"] for segment in r[0]["segments"]][0] # only one item because we update the route between each marker

    return reduce_line(all_coords)

def refresh_routes_from_markers(points: list[tuple[float, float]], hike_difficulty: int) -> list[list[tuple[float]]]:
    '''
    Return an unique list of coordinates that goes through every markers with (lat, lon) coordinates
    '''
    routes = []
    
    for i in range(len(points)-1):
        try:
            route = get_walk_from_markers(points[i:i+2], hike_difficulty)

            if route is not None:
                routes.append(route)
        except:
            traceback.print_exc()
            pass
        
    return routes