from dash import Input, Output, State, no_update
from utils.gpx import create_gpx
from components import ids
from app import app

@app.callback(Output(ids.DOWNLOAD_GPX, "data"),
            Output(ids.DOWNLOAD_BACK, "data"),
            Output(ids.DOWNLOAD_FORTH, "data"),
            Input(ids.EXPORT_BUTTON, 'n_clicks'),
            State(ids.STORE_CURRENT_ROUTE_DATA, "data"),
            State(ids.STORE_BACK, "data"),
            State(ids.STORE_FORTH, "data"))
def export(_: int, spec: dict, back: dict, forth: dict) -> tuple[dict, dict, dict]:
    '''
    Export GPX file with additional walks + forth and back GPX itineraries
    '''

    points = []
    points_back = []
    points_forth = []

    # Start with walk to go to the start. Lat lon order here
    if 'data' in forth.keys():
        legs = forth['data']['segments']
        for j,l in enumerate(legs):
            coords = l['geometrie']
            for i in range(len(coords)):
                t = (coords[i][0], coords[i][1])
                points_forth.append(t)
                if j == len(legs) - 1:
                    points.append(t)
    
    # Then add the main hike. Lon lat order here
    if 'coordinates' in spec.keys():
        route = spec["coordinates"]
        elevation = spec["elevation"]
        for i in range(len(route)):
            points.append((route[i][1], route[i][0], elevation[i]))

    # Finally add the finish walk to go to the bus stop. Lat lon order here
    if 'data' in back.keys():
        legs = back['data']['segments']
        for j,l in enumerate(legs):
            coords = l['geometrie']
            for i in range(len(coords)):
                t = (coords[i][0], coords[i][1])
                points_back.append(t)
                if j == 0:
                    points.append(t)

    # Export file
    return (dict(content=create_gpx(points), filename="randonnee.gpx"),
            dict(content=create_gpx(points_back), filename="itineraire_retour.gpx") if len(points_back) > 0 else no_update,
            dict(content=create_gpx(points_forth), filename="itinéraire_aller.gpx") if len(points_forth) > 0 else no_update) 