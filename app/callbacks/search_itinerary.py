from dash import html, Input, Output, State
from datetime import datetime
import traceback
from utils.date_time import unix_to_fr_date_hour
from utils.otp_tools import compute_itineraries_transit, add_walk_near_hike, stops_near_point
from components.layout_components import render_icon_modes
from components import ids
from app import app

def search(_date: datetime, _time: datetime, route: dict,
           maison: tuple[float, float], itineraries: dict, direction: int
           ) -> tuple[list[dict], int, dict, list[dict]]:
    '''
    Compute itineraries to go to start or from end of hike
    '''
    try:
        coords = route["features"][0]["geometry"]["coordinates"]
        if route["features"][0]["geometry"]["type"] == "Point":
            coords = [coords]

        def extreme(index_gpx):
            return coords[index_gpx]  
    
        depart = extreme(0)
        arrivee = extreme(-1)

        _time = datetime.strptime(_time, '%H:%M').time()
        _date = datetime.strptime(_date, '%Y-%m-%d')

        if direction == 0:
            points = [maison[::-1], depart]
        else:
            points = [arrivee, maison[::-1]]
        dic = compute_itineraries_transit(points, _time, _date)
        # if no itinerary is found or there are only walks
        if len(dic.keys()) == 0 or (len(dic.keys()) > 0 and True not in [it["is_transit"] for it in dic.values()]):
            its = []
            stops = set()
            for distance in range(1000, 10000, 1000):
                
                new_its, stops = search_itineraries_with_stops(depart, arrivee, maison, _time, _date, direction, distance, stops)
                # if we have results and at least one is not a strict walk, we end the search

                if len(new_its) > 0:
                    for new in new_its:
                        its.append(new)

                    if True in [it["is_transit"] for it in new_its]:
                        break
            
        # reindex itineraries
            dic = {}
            for i, it in enumerate(its):
                it["id"] = i
                dic[i] = it

            # keep only shortest walk
            walks = [it for it in its if len(set([s["mode"] for s in it["segments"]])) == 1]
            id_min = min(enumerate(walks), key=lambda x: x[1]["total_duree"])[1]["id"]
            for walk in walks:
                if int(walk["id"]) != int(id_min):
                    del dic[int(walk["id"])]
            
            # filter similar itineraries
            routes = set()
            for it in its:
                if it["id"] not in dic.keys():
                    continue
                new = ""
                for seg in it["segments"]:
                    if seg["is_transit"]:
                        new += seg["transit"]["route_id"]
                    else:
                        new += seg["mode"]
                new += unix_to_fr_date_hour(it["heure_depart"])
                if new in routes:
                    del dic[int(it["id"])]
                else:
                    routes.add(new)
        
        # sort by departure hour
        dic = dict(sorted(dic.items(), key=lambda item: item[1]["heure_depart"]))

        itineraries[direction] = dic

        options=[{'label': render_icon_modes(it), 'value': i} for i,it in dic.items()]

        return options, min(dic.keys()) if len(dic.keys()) > 0 else None, itineraries, html.Div(f'{len(dic)} itinéraires ont été trouvés.')
    
    except Exception as e:
        traceback.print_exc()
        return [], None, [], html.Div('Une erreur est survenue.')

@app.callback(Output(ids.DROPDOWN_ITINERARIES_FORTH, 'options'),
            Output(ids.DROPDOWN_ITINERARIES_FORTH, 'value'),
            Output(ids.STORE_ITINERARIES, 'data', allow_duplicate=True),
            Output(ids.PRINT_SEARCH_STATUS_FORTH, 'children'),    
            Input(ids.SEARCH_BUTTON_FORTH, 'n_clicks'),
            State(ids.DATE_PICKER_FORTH, 'date'),
            State(ids.TIME_PICKER_FORTH, 'value'),
            State(ids.LINE_HIKE,'data'),
            State(ids.MARKER_HOME, 'position'),
            State(ids.STORE_ITINERARIES, "data"))
def search_itineraries_forth(_: int, _date: datetime, _time: datetime, route: dict, 
           maison: tuple[float, float], itineraries: dict
           ) -> tuple[list[dict], int, dict, list[dict]]:

    return search(_date, _time, route, maison, itineraries, 0)

@app.callback(Output(ids.DROPDOWN_ITINERARIES_BACK, 'options'),
            Output(ids.DROPDOWN_ITINERARIES_BACK, 'value'),
            Output(ids.STORE_ITINERARIES, 'data'),
            Output(ids.PRINT_SEARCH_STATUS_BACK, 'children'),    
            Input(ids.SEARCH_BUTTON_BACK, 'n_clicks'),
            State(ids.DATE_PICKER_BACK, 'date'),
            State(ids.TIME_PICKER_BACK, 'value'),
            State(ids.LINE_HIKE,'data'),
            State(ids.MARKER_HOME, 'position'),
            State(ids.STORE_ITINERARIES, "data"))
def search_itineraries_back(_: int, _date: datetime, _time: datetime, route: dict, 
           maison: tuple[float, float], itineraries: dict
           ) -> tuple[list[dict], int, dict, list[dict]]:

    return search(_date, _time, route, maison, itineraries, 1)

######## UTILS

def search_itineraries_with_stops(depart: tuple[float, float], arrivee: tuple[float, float], maison: tuple[float, float],
                                  _time: datetime, _date: datetime, direction: int, distance: int, stops: set[str]) -> list[dict]:
    '''
    Compute itineraries from / to closest stops.
    Distance in meters, coordinates in (lon, lat) 
    '''
    all_stops = stops_near_point(depart if direction == 0 else arrivee, distance)

    its = []
    for stop in all_stops:
        if stop["id"] in stops:
            continue
        stops.add(stop["id"])
        if direction == 0:
            points = [maison[::-1], stop["lonlat"]]
        else:
            points = [stop["lonlat"], maison[::-1]]
        dico = compute_itineraries_transit(points, _time, _date)

    # flatten the values
        for it in dico.values():
            # compute the missing walk
            if direction == 0:
                points = [stop["lonlat"], depart]
            else:
                points = [arrivee, stop["lonlat"]]

            it = add_walk_near_hike(it, points, direction)

            its.append(it)

    return its, stops