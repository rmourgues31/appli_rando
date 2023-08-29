from dash import html, dcc, get_asset_url
from plotly.graph_objects import Figure, Layout, Scatter
import dash_bootstrap_components as dbc
from dash_extensions.javascript import Namespace
import dash_leaflet as dl
from datetime import datetime
from pathlib import Path
import pandas as pd
from utils.date_time import seconds_to_hour_min, unix_to_hour
from components import ids
from components import styles
from components.base_components import render_input, render_button, render_card, render_datepicker, render_dropdown, render_icon
from app import app # need this to load assets path for icons


def render_vertical_form(id_time: str, id_date: str, id_search: str) -> dbc.Form:
    '''
    Vertical form for a time picker, date picker, search button
    '''
    return dbc.Form([
                    html.Div([
                        dbc.Label("Heure de départ", html_for=id_time),
                        render_input(placeholder=None, value=datetime.strftime(datetime.now(), '%H:%M'), id=id_time)
                    ],
                    className="mb-3"),
                    html.Div([
                        dbc.Label("Date de départ", html_for=id_date),
                        render_datepicker(id=id_date)
                    ],
                    className="mb-3"),
                    render_button(id=id_search, text="Chercher")
                ])

def render_horizontal_form(id_time: str, id_date: str, id_search: str) -> dbc.Form:
    '''
    Horizontal form for a time picker, date picker, search button
    '''
    return dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Heure de départ", html_for=id_time),
                        render_input(placeholder=None, value=datetime.strftime(datetime.now(), '%H:%M'), id=id_time)
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.Label("Date de départ", html_for=id_date),
                        render_datepicker(id=id_date)
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        render_button(id=id_search, text="Chercher")
                    ]
                )
            ],
            #className="g-3",
            align="end",
            justify="center"
        )

def render_tab(id_time: str, id_date: str, id_search: str, id_search_status: str, 
               id_dropdown: str, id_text_data: str, title_tab: str) -> dbc.Tab:
    '''
    Tab for form input
    '''
    return dbc.Tab(render_card([
                    #html.Br(),
                    render_horizontal_form(id_time, id_date, id_search),
                    html.Hr(),
                    dbc.Label("Résultats", html_for=id_dropdown),
                    html.Div(id=id_search_status),
                    render_dropdown(id=id_dropdown, options=[], value=None),
                    html.Div(render_card([
                            dcc.Markdown(id=id_text_data),
                            dcc.Clipboard(
                                target_id=id_text_data,
                                style={
                                    "position": "absolute",
                                    "top": 0,
                                    "right": 20,
                                    "fontSize": 20,
                                },
                            )
                        ]))
                ]), 
                label=title_tab
            )

def render_icon_modes(it: dict) -> html.Span:
    '''
    Build a label to display for itinerary
    '''
    height = 15
    base_path = "icons/"
    
    div = [html.A(f'{unix_to_hour(it["heure_depart"])} - {unix_to_hour(it["heure_arrivee"])} | '),
            html.Img(src=get_asset_url(base_path + "clock_icon.png"), height=height),
            html.A(f' {seconds_to_hour_min(it["total_duree"])} | ')]
    for leg in it["segments"]:
        match leg["mode"]:
            case "WALK":
                source = base_path + "walk_icon.png"
            case "BUS":
                source = base_path + "bus_icon.png"
            case "TRAM":
                source = base_path + "tram_icon.png"
            case "RAIL":
                source = base_path + "train_icon.png"
            case _:
                source = base_path + "unknown_icon.png"
        div.append(html.Img(src=get_asset_url(source), height=height))

    return html.Span(div , style={'align-items': 'center', 'justify-content': 'center'})

def render_home_icon():
    return render_icon('house_icon.png', 0.5)

def render_geojson_stops():
    '''
    Display all stops of agencies as a geojson
    '''
    ns = Namespace('dashExtensions','default')
    path = "." + get_asset_url("geojson")

    files = list(Path(path).rglob('*.geojson'))
    return [dl.GeoJSON(url=str(file), 
                       cluster=True, 
                       zoomToBoundsOnClick=True,
                       options=dict(pointToLayer=ns('point_to_layer')),  # how to draw points
                       hideout=dict(circleOptions=dict(fillOpacity=1, stroke=False, radius=5))
                    ) for file in files]

def render_empty_figure():
    data = []
    for name, uid, color in [
        ("Randonnée", ids.UID_HIKE, styles.BLUE),
        ("Avant", ids.UID_FORTH, styles.GREEN),
        ("Après", ids.UID_BACK, styles.RED)
        ]:
        data.append(Scatter(x=[], 
                            y=[], 
                            line={"width": 4, "color": color}, 
                            marker={"color": color},
                            name = name, 
                            hovertemplate='<b>Distance</b>: %{x:.2f} km<br><b>Altitude</b>: %{y:.0f} m',
                            uid=uid))
        
    return Figure(layout=Layout(
                        hovermode="x", 
                        margin=dict(l=20, r=20, t=20, b=20),
                        xaxis=dict(ticksuffix=" km"),
                        yaxis=dict(ticksuffix=" m")),
                data=data)
    
def load_hikes_from_csv():
    '''
    Return a DataFrame containing the hikes stored in CSV file
    '''
    hike_df = pd.read_csv("." + get_asset_url("csv/camptocamp.csv"))

    def func(x):
        return f'[{x["name"]}](https://www.camptocamp.org/routes/{x["id"]})'
    
    hike_df["name"] = hike_df.apply(func,axis=1)
    
    hike_df.set_index('id', inplace=True, drop=False)
    return hike_df