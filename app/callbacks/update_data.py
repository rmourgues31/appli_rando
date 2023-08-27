from dash import Input, Output
from dash.exceptions import PreventUpdate
from utils.route_spec import refresh_spec
from components import ids
from app import app

@app.callback(Output(ids.STORE_CURRENT_ROUTE_DATA, "data", allow_duplicate=True),
              Input(ids.LINE_HIKE, "data"))
def update_spec(geojson: dict) -> dict:
    '''
    Upon modification of hike, update the global specs of the hike. 
    '''

    if not geojson:
        coords = None
    else:
        coords = geojson["features"][0]["geometry"]["coordinates"]

        if geojson["features"][0]["geometry"]["type"] == "Point":
            coords = [coords]

    return refresh_spec(coords) 

@app.callback(Output(ids.DROPDOWN_ITINERARIES_FORTH, 'options', allow_duplicate=True),
              Output(ids.DROPDOWN_ITINERARIES_FORTH, 'value', allow_duplicate=True),
              Output(ids.PRINT_SEARCH_STATUS_FORTH, 'children', allow_duplicate=True),
              Output(ids.DROPDOWN_ITINERARIES_BACK, 'options', allow_duplicate=True),
              Output(ids.DROPDOWN_ITINERARIES_BACK, 'value', allow_duplicate=True),
              Output(ids.PRINT_SEARCH_STATUS_BACK, 'children', allow_duplicate=True),
              Output(ids.STORE_ITINERARIES, 'data', allow_duplicate=True),
              Input(ids.STORE_CURRENT_ROUTE_DATA, "data"))
def reset(spec: dict) -> tuple[list, list, list, list, list, list, dict]:
    '''
    '''

    if spec == {}:
        return [], None, [], [], None, [], {}
    else:
        raise PreventUpdate