from dash import Input, Output, State, no_update, get_asset_url
from dash_leaflet import Marker
import pandas as pd
import json
from components import ids
from components.layout_components import render_icon, load_hikes_from_csv
from utils.gpx import gpx_from_upload_component, extract_route
from utils.tools import reverse_list_in_list, flatten_list_of_list
from utils.valhalla_tools import refresh_routes_from_markers
from app import app

hike_df = load_hikes_from_csv()

def geojson_from_coords(coords: list[tuple[float, float]], geom_type: str) -> dict:
    """
    Build a geojson for one feature from (lon, lat) coordinates
    """
    return {
            'type': 'FeatureCollection', 
            'features': [{
                'type': 'Feature',
                'geometry': {
                    'type': geom_type, 
                    'coordinates': coords
                }
            }]
        }

@app.callback(
    Output(ids.LINE_HIKE, "data", allow_duplicate=True),
    Output(ids.MODAL_EXAMPLES, "is_open", allow_duplicate=True),
    Input(ids.TABLE_EXAMPLES, 'active_cell'))
def load_from_table(active_cell):
    '''
    Upload a hike on map based on examples table
    '''
    active_row_id = active_cell['row_id'] if active_cell else None

    coords = json.loads(hike_df.loc[active_row_id, "coordinates"])

    geom_type = hike_df.loc[active_row_id, "type"]
    if geom_type != "Point":
        coords = reverse_list_in_list(coords)
    else:
        coords = coords[::-1]
    return geojson_from_coords(coords, geom_type), False

@app.callback(Output(ids.LINE_HIKE, "data", allow_duplicate=True),
              Output(ids.ALERT_UPLOAD_ERROR, "is_open"),
              Input(ids.UPLOAD, 'contents'))
def add_gpx(gpx_content: str) -> tuple[dict, bool]:
    '''
    If user uploads a gpx, display on the map
    '''

    try:
        gpx = gpx_from_upload_component(gpx_content)
        coords = extract_route(gpx)
        return geojson_from_coords(coords), False
    
    except:
        # file may not be a gpx or other reason
        return no_update, True
    

@app.callback(Output(ids.LINE_HIKE, "data"), 
              Input(ids.EDIT_CONTROL, "geojson"),
              Input(ids.SLIDER_DIFFICULTY, "value"))
def edit_geojson(geojson: dict, hike_difficulty: int) -> dict:
    '''
    Upon add / modification with EditControl, update the hike
    '''
    
    if (geojson is None or len(geojson["features"]) == 0):
        return None
    
    feature = geojson["features"][0]
    feature["properties"]["source"] = ids.EDIT_CONTROL
    
    if feature["geometry"]["type"] == "LineString":
        # coordinates in geojson are the waypoints
        points = reverse_list_in_list(feature["geometry"]["coordinates"])
        coords = refresh_routes_from_markers(points, hike_difficulty)
        feature["geometry"]["coordinates"] = reverse_list_in_list(flatten_list_of_list(coords))

    return geojson

@app.callback(Output(ids.EDIT_CONTROL, "draw"),
              Output(ids.UPLOAD, "disabled"),
              Output(ids.SEARCH_BUTTON_FORTH, "disabled"),
              Output(ids.SEARCH_BUTTON_BACK, "disabled"),
              Input(ids.LINE_HIKE, "data"))
def hide_controls(geojson: dict) -> tuple[dict, bool, bool, bool]:
    '''
    Upon modification with EditControl or GPX upload, update the visibility of buttons: draw, upload, itinerary search back and forth
    '''

    if (geojson is None or len(geojson["features"]) == 0): # no geojson at all
        return dict(polygon=False, circle=False, rectangle=False, circlemarker=False), False, True, True
    elif "source" in geojson["features"][0]["properties"].keys(): # geojson comes from edit control : only allow search. Need to erase the drawing before drawing or uploading
        return dict(polyline=False, marker=False, polygon=False, circle=False, rectangle=False, circlemarker=False), True, False, False
    else: # geojson comes from upload: allow drawing and upload to erase the gpx file
        return dict(polygon=False, circle=False, rectangle=False, circlemarker=False), False, False, False

@app.callback(Output(ids.LAYER_TRACE, "children"),
              Input(ids.LINE_HIKE, "data"),
              State(ids.LAYER_TRACE, "children"))
def add_start_end(geojson: dict, children: list[dict]) -> list[dict]:
    '''
    Upon modification with EditControl or GPX upload, add start / end markers
    '''

    if (geojson is None or len(geojson["features"]) == 0 or geojson["features"][0]["geometry"]["type"] == "Point"):
        return children
    coord = geojson["features"][0]["geometry"]["coordinates"]
    
    if len(coord) > 1:
        start = Marker(position=coord[0][::-1], icon=render_icon("start_icon.png", 0.5))
        end = Marker(position=coord[-1][::-1], icon=render_icon("finish_icon.png", 0))
        if len(children) > 1:
            children[1] = start
            children[2] = end
        else:
            children.append(end)
            children.append(start)
    return children