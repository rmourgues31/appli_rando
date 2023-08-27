
import dash_leaflet as dl
from dash import Input, Output, State, dcc, get_asset_url, no_update
from utils.date_time import seconds_to_hour_min, unix_to_fr_date_hour, iso_to_fr_date_hour
from utils.geo import distance_to_string, distance_km
from utils.template_fill import fill_template
from utils.elevation import compute_elevation_gain, get_alti
from utils.tools import reverse_list_in_list
from components import ids, styles
from app import app

@app.callback(Output(ids.STORE_BACK, "data"),
              Output(ids.STORE_ITINERARIES, "data", allow_duplicate=True),
              Input(ids.DROPDOWN_ITINERARIES_BACK, "value"),
              State(ids.STORE_ITINERARIES, "data"))
def update_chosen_back(value: int, itineraries: dict) -> tuple[dict,dict]:
    return update_chosen(value, itineraries, 1)

@app.callback(Output(ids.STORE_FORTH, "data"),
              Output(ids.STORE_ITINERARIES, "data", allow_duplicate=True),
              Input(ids.DROPDOWN_ITINERARIES_FORTH, "value"),
              State(ids.STORE_ITINERARIES, "data"))
def update_chosen_forth(value: int, itineraries: dict) -> tuple[dict, dict]:
    return update_chosen(value, itineraries, 0)

def update_chosen(value: int, itineraries: dict, direction: int) -> tuple[dict, dict]:
    '''
    Given a chosen itinerary, update the store and compute the specs of the walk.
    '''

    if value is None or str(direction) not in itineraries.keys() or str(value) not in itineraries[str(direction)].keys():
        return {}, no_update
    chosen = itineraries[str(direction)][str(value)]
    if "added_cum_distance" not in chosen.keys():
        index = -1 if direction == 0 else 0
        leg = chosen['segments'][index]
        if leg['mode'] in ['WALK', 'pedestrian']:
            coords = reverse_list_in_list(leg['geometrie'])
            alti = get_alti(coords)
            dist = distance_km(coords)
        else:
            alti = []
            dist = []
        chosen["added_cum_distance"] = dist
        chosen["added_elevation"] = alti
        chosen["added_elevation_gain"] = compute_elevation_gain(alti)
        
    return {"value": value, "data": chosen}, itineraries


@app.callback(
    Output(ids.LINE_ROUTE_FORTH, 'children'),
    Output(ids.TEXT_DATA_ITINERARY_FORTH, 'children'),
    Input(ids.STORE_FORTH, 'data'))
def display_itinerary_forth(itinerary: dict) -> tuple[list[dl.Polyline], list]:
    return display_itinerary(itinerary, 0)

@app.callback(
    Output(ids.LINE_ROUTE_BACK, 'children'),
    Output(ids.TEXT_DATA_ITINERARY_BACK, 'children'),
    Input(ids.STORE_BACK, "data"))
def display_itinerary_back(itinerary: dict) -> tuple[list[dl.Polyline], list, dict]:
    return display_itinerary(itinerary, 1)

def display_itinerary(itinerary: dict, direction: int) -> tuple[list[dl.Polyline], list]:
    '''
    Display selected itinerary on the map
    '''
    if itinerary == {}:
        return [], ""
    chosen = itinerary["data"]

    summary = {
        'departure_time': unix_to_fr_date_hour(chosen["heure_depart"]),
        'arrival_time': unix_to_fr_date_hour(chosen["heure_arrivee"]),
        'total_duration': seconds_to_hour_min(chosen["total_duree"]),
        'walk_time': seconds_to_hour_min(chosen["total_temps_marche"]),
        'walk_distance': distance_to_string(chosen["total_distance_marche"]),
        'transit_time': seconds_to_hour_min(chosen["total_temps_transports"]),
        'waiting_time': seconds_to_hour_min(chosen["total_temps_attente"])
    }

    result = fill_template("." + get_asset_url("markdown/itinerary_description.md"), summary)
    global_desc = [result, "##### Étapes"]

    legs = []      
    for i, l in enumerate(chosen['segments']):

        if i == len(chosen["segments"]) - 1 and direction == 0 :
            color = styles.GREEN
        elif i == 0 and direction == 1:
            color = styles.RED 
        else:
            color = styles.BLACK
        
        coords = l['geometrie']
        variables = {
            'duration': seconds_to_hour_min(l["temps"]),
            'distance': distance_to_string(l["distance"]),
            'departure_time': unix_to_fr_date_hour(l["heure_depart"]),
            'arrival_time': unix_to_fr_date_hour(l["heure_arrivee"])
        }
        file = "." + get_asset_url("markdown/walk_leg_description.md")
        if l['mode'] != "WALK":
            file = "." + get_asset_url("markdown/transit_leg_description.md")
            route = l['transit']
            color = "#" + route["color"]
            sub_var = {
                'mode': l["mode"],
                "short_name": route["short_name"],
                "long_name": route["long_name"],
                "agency_name": route["agency_name"],
                "departure_stop": route["arret_depart"],
                "arrival_stop": route["arret_arrivee"]
            }
            variables = dict(variables, **sub_var)
        leg_summary = fill_template(file, variables)

        line = dl.Polyline(positions= coords, 
                           fill= False, 
                           color=color,
                           children=dl.Tooltip(dcc.Markdown(leg_summary, style={"white-space": "pre"}), sticky=True),
                           dashArray= '10, 10',
                           weight=5)
        
        legs.append(line)
        global_desc.append(leg_summary)
    
    return legs, '\n\n'.join(global_desc)