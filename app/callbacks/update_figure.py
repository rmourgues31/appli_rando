from dash import Input, Output, State, Patch
from utils.geo import distance_to_string
from components import ids
from app import app

@app.callback(Output(ids.DESC_HIKE, "children"),
              Input(ids.STORE_CURRENT_ROUTE_DATA, "data"),
              Input(ids.STORE_BACK, "data"),
              Input(ids.STORE_FORTH, "data"))
def update_desc_hike(specs: dict, data_forth: dict, data_back: int) -> str:
    '''
    Update distance and elevation gain on Figure description
    '''

    if len(specs.keys()) == 0:
        d = e = 0
    else:
        d = specs["total_dist"]
        e = specs["elevation_gain"]
        
        for dic in [data_forth, data_back]:
            if dic != {}:
                dist = dic["data"]["added_cum_distance"]
                elev = dic["data"]["added_elevation_gain"]
                d += dist[-1]
                e += elev
    
    return f'Distance : {distance_to_string(d*1000)}, D+ : {e} m'


@app.callback(Output(ids.GRAPH_PROFILE, "figure"),  
              Input(ids.STORE_CURRENT_ROUTE_DATA, "data"))
def update_profile(spec: dict) -> Patch:
    '''
    When the hiking track is changed, update elevation profile
    '''

    if spec == {}:
        dist = []
        elev = []
    else:
        dist = spec["cum_distance"]
        elev = spec["elevation"]

    return update_fig_gen(0, dist, elev)

@app.callback(Output(ids.GRAPH_PROFILE, "figure", allow_duplicate=True),  
              Input(ids.STORE_BACK, "data"),
              State(ids.STORE_CURRENT_ROUTE_DATA, "data"))
def update_figure_back(itinerary: dict, spec_hike: dict) -> Patch:
    '''
    When the back itinerary is changed, update elevation profile
    '''
    return update_figure(itinerary, spec_hike, 1, 2)

@app.callback(Output(ids.GRAPH_PROFILE, "figure", allow_duplicate=True),  
              Input(ids.STORE_FORTH, "data"),
              State(ids.STORE_CURRENT_ROUTE_DATA, "data"))
def update_figure_forth(itinerary: dict, spec_hike: dict) -> Patch:
    '''
    When the forth itinerary is changed, update elevation profile
    '''
    return update_figure(itinerary, spec_hike, 0, 1)

def update_figure(itinerary: dict, spec_hike: dict, direction: int, index: int) -> Patch:
    '''
    When an itinerary is changed, update the elevation profile of start / end
    '''

    if itinerary == {}:
        return update_fig_gen(index, [], [])
    
    chosen = itinerary["data"]

    dist = chosen["added_cum_distance"]
    elev = chosen["added_elevation"]
    
    if direction == 0:
        x = [di - dist[-1] for di in dist]
    else:
        x = [di + spec_hike["total_dist"] for di in dist]

    return update_fig_gen(index, x, elev)

def update_fig_gen(index: str, dist: list[float], elev: list[int]) -> Patch:
    '''
    Update the figure.
    Index: index of the data for the Patch. See components.render_empty_figure() for order
    '''
    
    mode = "lines" if len(dist) > 1 else "lines+markers"
    patch = Patch()
    patch["data"][index]["x"] = dist
    patch["data"][index]["y"] = elev
    patch["data"][index]["mode"] = mode
    
    #if len(elev) > 0:
        #y_range = [0, axis_alti(max(elev))]
        #fig.update_layout(yaxis_range=y_range, yaxis_autorange=False)

    return patch