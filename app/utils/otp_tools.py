import polyline
import requests
import json
import os
import traceback
from datetime import datetime
from utils.geo import reduce_line, distance_km
from utils.date_time import unix_to_datetime

otp_url = "http://" + os.getenv("OTP_SERVICE") + ":" + os.getenv("OTP_PORT")
walk_speed = 1.33

def query(json_data: dict) -> dict:
    '''
    Query on GraphQL endpoint
    '''
    response = requests.post(f'{otp_url}/otp/routers/default/index/graphql', json=json_data)
    data = json.loads(response.content)["data"]
    return data

def get_itinerary(fromPlace: tuple[float, float], toPlace: tuple[float, float], 
                  modes: list[str], _time: datetime, _date: datetime) -> dict:
    '''
    Get a route using different modes
    https://docs.opentripplanner.org/en/dev-2.x/RouteRequest/ 
    http://localhost:8080/graphiql 
    '''

    if _date is None:
        _date = datetime.today()
    if _time is None:
        _time = datetime.now()

    json_data = {"query":
    '''
    query ($from_lat: Float!, $from_lon: Float!, $to_lat: Float!, $to_lon: Float!, $date: String!, $time: String!, $numItineraries: Int, $modes: [TransportMode]!, $searchWindow: Long!, $walkSpeed: Float!) {
        plan(
            from: {lat: $from_lat, lon: $from_lon}
            to: {lat: $to_lat, lon: $to_lon}
            date: $date
            time: $time
            numItineraries: $numItineraries
            transportModes: $modes
            searchWindow: $searchWindow
            walkSpeed: $walkSpeed
        ) {
            itineraries {
                startTime
                endTime
                walkTime
                walkDistance
                waitingTime
                duration
                legs {
                    mode
              			transitLeg
                    duration
                    distance
                    legGeometry {
                        points
                    }
                    from {
                        stop {
                            name
                        }
                        }
                    to {
                        stop {
                            name
                        }
                    }
                    startTime
                    endTime
                    intermediateStops {
                        name
                    }
                    route {
                        gtfsId
                        shortName
                        longName
                        mode
                        color
                        bikesAllowed
                      	agency {
                        	name
                      }
                    }
                }
            }
        }
    }
    ''',
    "variables": {
        'from_lat': fromPlace[1],
        'from_lon': fromPlace[0],
        'to_lat': toPlace[1],
        'to_lon': toPlace[0],
        'date': _date.strftime("%Y-%m-%d"), 
        'time': _time.strftime('%H:%M:%S'),
        'numItineraries': 10,
        'searchWindow': 10000,
        'modes': [{'mode': m} for m in modes],
        'walkSpeed': walk_speed
        }
    }

    return query(json_data)

def compute_itineraries_transit(points: list[tuple[float, float]], _time: datetime, _date: datetime) -> dict:
    '''
    Compute an itinerary using public transport and walk, for (lon, lat) points
    Return a dict with main data {'itinerary_id': {__data__}}
    '''
    
    return compute_itineraries(points, _time, _date, ["TRANSIT", "WALK"])

def compute_itineraries_walk(points: list[tuple[float, float]], _time: datetime, _date: datetime) -> dict:
    '''
    Compute an itinerary using walk, for (lon, lat) points
    Return a dict with main data {'itinerary_id': {__data__}}
    '''
    
    return compute_itineraries(points, _time, _date, ["WALK"])

def compute_itineraries(points: list[tuple[float, float]], _time: datetime, _date: datetime, modes: list[str]) -> dict:
    '''
    Compute an itinerary, for (lon, lat) points
    Return a dict with main data {'itinerary_id': {__data__}}
    '''

    depart = points[0]
    arrivee = points[1]
    
    content = get_itinerary(depart, arrivee, modes, _time, _date)
    itins = content['plan']['itineraries']

    dic = {}
    for i, itin in enumerate(itins):
        legs = itin['legs']
        segs = []
        is_transit = False
        for l in legs:
            
            seg = {
                'mode': l["mode"],
                'temps': l['duration'],
                'distance': l['distance'],
                'geometrie': reduce_line(polyline.decode(l['legGeometry']['points'])),
                'heure_depart': l['startTime'],
                'heure_arrivee': l['endTime'],
                'is_transit': l["transitLeg"]
            }
            if l["transitLeg"]:
                is_transit = True
                route = l["route"]
                r = {
                    'color': route["color"],
                    'route_id': route['gtfsId'],
                    'long_name': route["longName"],
                    'short_name': route["shortName"],
                    'arret_depart': l["from"]["stop"]["name"],
                    'arret_arrivee': l["to"]["stop"]["name"] ,
                    'agency_name': route["agency"]["name"]                  
                }
                seg['transit'] = r
            segs.append(seg)
        it = {
                'id': i,
                'heure_depart': itin['startTime'],
                'heure_arrivee': itin['endTime'],
                'total_duree': itin['duration'],
                'total_temps_marche': itin["walkTime"],
                'total_distance_marche': itin["walkDistance"],
                'total_temps_transports': itin["duration"] - itin["walkTime"] - itin["waitingTime"],
                'total_temps_attente': itin["waitingTime"],
                'is_transit': is_transit,
                "segments": segs
            }
        dic[i] = it
    return dic

def stops_near_point(point: tuple[float, float], radius: int) -> list[dict]:
    '''
    Return all stops within {radius} meters of the desired point (lon, lat)
    '''
    json_data = {"query":
    '''
    query ($lat: Float!, $lon: Float!, $radius: Int!) {
        stopsByRadius(
            lat: $lat,
            lon: $lon,
            radius: $radius
        ) {
            edges {
                node {
                    distance
                    stop {
                        gtfsId
                        lat
                        lon
                        name
                        cluster {
                            gtfsId
                        }
                    }
                }
            }
        }
    }
    ''',
    "variables": {
        "lat": point[1],
        "lon": point[0],
        "radius": radius
        }
    }

    data = query(json_data)
    
    stops = {}

    for edge in data["stopsByRadius"]["edges"]:

        stop = edge["node"]["stop"]
        stop_id = stop["gtfsId"]
        if stop_id in stops.keys() or (stop["cluster"] and stop['cluster']["gtfsId"] == stop_id) or not stop["cluster"]:
            stops[stop_id] = {"id": stop_id, "lonlat": (stop["lon"], stop["lat"]), "name": stop["name"], "dist": edge["node"]["distance"]}
        elif stop["cluster"]:
            stops[stop["cluster"]["gtfsId"]] = {}


    result = list(stops.values())
    return result

def add_walk_near_hike(itin: dict, points: tuple[tuple[float, float]], direction: int):
    '''
    Add a walk segment at the beginning or end of the itinerary. Update route data.
    Parameters
        - itin: itinerary as returned by the itin_to_dict function
        - points: (lon, lat) start & end
        - direction: direction of the itinerary
    '''
    try:
        
        line = compute_itineraries_walk(points, None, None)

        hike = line[0]["segments"][0]["geometrie"]
        dist = distance_km(hike)
        seg = {
                    'mode': "WALK",
                    'temps': int(dist[-1]*1000 / walk_speed),
                    'distance': round(dist[-1]*1000,1),
                    'geometrie': hike
                }
        if direction == 0:
            seg["heure_depart"] = itin["heure_arrivee"]
            itin["heure_arrivee"] += seg["temps"] * 1000
            seg["heure_arrivee"] = itin["heure_arrivee"]
            last_segment = itin["segments"][-1]
            
            if last_segment["is_transit"]:
                itin["segments"].append(seg)
            else:
                last_segment["temps"] += seg["temps"]
                last_segment["heure_arrivee"] += seg["temps"] * 1000
                last_segment["distance"] += seg["distance"]
                last_segment["geometrie"] += seg["geometrie"]
        else:
            seg["heure_arrivee"] = itin["heure_depart"]
            itin["heure_depart"] -= seg["temps"] * 1000
            seg["heure_depart"] = itin["heure_depart"]
            first_segment = itin["segments"][0]

            if first_segment["is_transit"]:
                itin["segments"].insert(0, seg)
            else:
                first_segment["temps"] += seg["temps"]
                first_segment["heure_depart"] -= seg["temps"] * 1000
                first_segment["distance"] += seg["distance"]
                first_segment["geometrie"] = seg["geometrie"] + first_segment["geometrie"]

        itin["total_temps_marche"] += seg["temps"]
        itin["total_distance_marche"] += seg["distance"]
            
        return itin
    
    except Exception as e:
        traceback.print_exc()
        return itin

def get_agencies() -> list[dict]:
    '''
    Get all agencies in the GTFS feeds
    '''
    json_data = {
        "query": 
        '''
            query agencies {
                agencies {
                    gtfsId
                    name
                    url
                    }
                }
        '''
    }
    
    return query(json_data)["agencies"]