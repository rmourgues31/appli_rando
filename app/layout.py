import dash_leaflet as dl
from dash import html, dcc, get_asset_url, dash_table
import dash_bootstrap_components as dbc
from utils.otp_tools import get_agencies
from components.base_components import render_button, render_modal, render_upload
from components.layout_components import render_tab, render_home_icon, render_geojson_stops, render_empty_figure, load_hikes_from_csv
from components import ids

####################
## DIFFICULTY DIV ##
####################

with open("." + get_asset_url("markdown/difficulty_tooltip.md"), "r", encoding="UTF8") as f:
    diff_tooltip = f.read()

difficulty = html.Div(id=ids.DIV_DIFFICULTY, children=[
                    html.Div(children=[
                        dbc.Label("Technicité", html_for=ids.SLIDER_DIFFICULTY),
                        html.Img(src=get_asset_url("icons/question_icon.png"), height=20, id=ids.HELP_DIFFICULTY)
                        ], id=ids.TOOLTIP_DIFFICULTY),
                    dcc.Slider(id=ids.SLIDER_DIFFICULTY, min=1, max=6, step=1, marks={i:f'T{i}' for i in range(1,7)}, value=1),
                    dbc.Tooltip(children=[dcc.Markdown(diff_tooltip, link_target="_blank")],target=ids.HELP_DIFFICULTY, trigger="legacy"
                    ),
                ])

####################
## CONTROL INPUTS ##
####################

inputs = html.Div(className="overflow-scroll", style={"width": "444px"}, children=[
            render_upload(ids.UPLOAD),
            dbc.Alert(
                    "Ce fichier n'est pas reconnu comme GPX. Aucune modification n'a été faite.",
                    id=ids.ALERT_UPLOAD_ERROR,
                    is_open=False,
                    duration=4000,
                    color="warning"
                ),
            html.Hr(),
            dbc.Form(difficulty),
            html.Hr(),
            dbc.Tabs([
                render_tab(ids.TIME_PICKER_FORTH, ids.DATE_PICKER_FORTH, ids.SEARCH_BUTTON_FORTH, ids.PRINT_SEARCH_STATUS_FORTH, 
                           ids.DROPDOWN_ITINERARIES_FORTH, ids.TEXT_DATA_ITINERARY_FORTH, "Aller", ids.DIV_RESULTS_FORTH),
                render_tab(ids.TIME_PICKER_BACK, ids.DATE_PICKER_BACK, ids.SEARCH_BUTTON_BACK, ids.PRINT_SEARCH_STATUS_BACK, 
                           ids.DROPDOWN_ITINERARIES_BACK, ids.TEXT_DATA_ITINERARY_BACK, "Retour", ids.DIV_RESULTS_BACK)
            ]),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div([
                            render_button(id=ids.EXPORT_BUTTON, text="Exporter tout"),
                            dcc.Download(id=ids.DOWNLOAD_GPX),
                            dcc.Download(id=ids.DOWNLOAD_FORTH),
                            dcc.Download(id=ids.DOWNLOAD_BACK)
                        ])
                    ]
                )
            )
        ])

####################
## MAP & GRAPH ##
####################

map_content = dl.Map([dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                              activeColor="#214097", completedColor="#972158"),
                    dl.LayersControl(
                        [
                            dl.BaseLayer(dl.TileLayer(attribution="OpenStreetMap"), name="Carte normale", checked=True),
                            dl.BaseLayer(dl.TileLayer(url="http://a.tile.opentopomap.org/{z}/{x}/{y}.png", attribution="OpenTopoMap"), name="Carte topographique"),
                            dl.Overlay(dl.LayerGroup(render_geojson_stops()), name="Arrêts des lignes de transport", checked=False),
                            dl.Overlay(dl.Marker(id=ids.MARKER_HOME, position=(45.237111, 5.672899), draggable=True, icon=render_home_icon()), name="Maison", checked=True),
                            dl.Overlay(dl.LayerGroup([dl.FeatureGroup([
                                dl.EditControl(
                                    id=ids.EDIT_CONTROL,
                                    draw=dict(polygon=False, circle=False, rectangle=False, circlemarker=False),
                                    position="topleft"
                                )])]), name="Édition de la trace", checked=True),
                            dl.Overlay(dl.LayerGroup([dl.GeoJSON(id=ids.LINE_HIKE)], id=ids.LAYER_TRACE), name="Trace", checked=True),
                            dl.Overlay(dl.LayerGroup(id=ids.LINE_ROUTE_FORTH), name="Itinéraire aller", checked=True),
                            dl.Overlay(dl.LayerGroup(id=ids.LINE_ROUTE_BACK), name="Itinéraire retour", checked=True)
                        ])
                    ],
                    center = [45.204793, 5.5], zoom = 9, id=ids.MAP, style={'height': '100%'})

figure = render_empty_figure()

profile_graph = dcc.Graph(id=ids.GRAPH_PROFILE, 
                        figure= figure,
                        style={"height": "170px"}
                        )

####################
## MODALS ##
####################

with open("." + get_asset_url("markdown/tutorial.md"), "r", encoding="UTF8") as f:
    howto_md = f.read()

tutorial_modal = render_modal(id=ids.MODAL_TUTORIAL,
                            title="Tutoriel",
                            content=[dcc.Markdown(howto_md)], 
                            close_id=ids.CLOSE_TUTORIAL)

agencies_modal = render_modal(id=ids.MODAL_AGENCIES, 
                                        title="Opérateurs",
                                        content=[
                                            html.P("Liste des opérateurs fournie dans les données GTFS"),
                                            html.Ul([html.Li(html.A(c["name"], href = c["url"], target = "_blank")) for c in get_agencies()])
                                        ], 
                                        close_id=ids.CLOSE_AGENCIES)

credits_modal = render_modal(id=ids.MODAL_CREDITS,
                            title="Crédits",
                            content=
                                html.Ul([html.Li(html.A(c[0], href=c[1], target="_blank")) for c in [
                                    ("Valhalla", "https://github.com/valhalla/valhalla"),
                                    ("GIS•OPS", "https://github.com/gis-ops"),
                                    ("Open Trip Planner", "https://github.com/opentripplanner/OpenTripPlanner"),
                                    ("Open Street Map", "https://openstreetmap.com"),
                                    ("BD Alti", "https://geoservices.ign.fr/bdalti "),
                                    ("Camptocamp", "https://www.camptocamp.org"),
                                    ("Icons8", "https://icons8.com")
                                    ]]), 
                            close_id=ids.CLOSE_CREDITS)

hike_df = load_hikes_from_csv()
example_modal = render_modal(id=ids.MODAL_EXAMPLES,
                             title="Randonnées existantes",
                            
                             content = [
                                 dcc.Markdown("- Cliquez sur un lien pour ouvrir le topo. \n - Cliquez sur une ligne pour charger l'itinéraire. \n - Les données présentées sont sous licence [CC by-sa](https://www.camptocamp.org/articles/106728/fr/licences-des-contenus#cc-by-sa).", link_target="_blank"),
                                 dash_table.DataTable(
                                            id=ids.TABLE_EXAMPLES,
                                            columns=[
                                                {"name": "Nom", "id": "name", 'presentation': 'markdown'},
                                                {"name": "Difficulté", "id": "rating"},
                                                {"name": "Zone", "id": "areas"}
                                            ],
                                            tooltip_data=[
                                                {
                                                    "name": {'value': f"Auteur : {row['author']}", 'type': 'markdown'}
                                                } for row in hike_df.to_dict('records')
                                            ],
                                            style_cell={'textAlign': 'left'},
                                            data=hike_df.to_dict('records'),
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrer..."},
                                            sort_action="native",
                                            sort_mode="multi",
                                            page_size= 10,
                                        )
                             ],
                            close_id=ids.CLOSE_EXAMPLES)

####################
## HEADER ##
####################

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=get_asset_url("favicon.ico"),
                            height="30px",
                        ),
                        align="start"
                    ),
                    dbc.Col(
                        [
                            html.H3("Itirando")
                        ],
                        align="baseline"
                    ),
                     dbc.Col(
                        [
                            html.P("La randonnée en transports en commun")
                        ],
                        align="baseline",
                        md="auto"
                    )
                ],
                align="start",
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.NavItem(render_button(id=ids.OPEN_EXAMPLES, text="Randonnées"))),
                    dbc.Col(dbc.NavItem(render_button(id=ids.OPEN_TUTORIAL, text="Tutoriel"))),
                    dbc.Col(dbc.NavItem(render_button(id=ids.OPEN_AGENCIES, text="Opérateurs"))),
                    dbc.Col(dbc.NavItem(render_button(id=ids.OPEN_CREDITS, text="Crédits"))),
                    example_modal,
                    tutorial_modal,
                    agencies_modal,
                    credits_modal
                ],
                align="start",
                justify="evenly"
            )
        ],
        fluid=True
    )
)


####################
## LOADER ##
####################

loader = dcc.Loading([
    # STORE DATA
    dcc.Store(id=ids.STORE_ITINERARIES, data={}),
    dcc.Store(id=ids.STORE_BACK, data = {}),
    dcc.Store(id=ids.STORE_FORTH, data = {}),
    dcc.Store(id=ids.STORE_CURRENT_ROUTE_DATA, data={}),
    dcc.Store(id=ids.STORE_BUFFER_INSERTION, data={}),
])


####################
## LAYOUT ##
####################

layout = html.Div(
    className="vh-100 d-flex flex-column",
    children=[
        header,
        html.Div(
            className="d-flex flex-fill overflow-hidden",
            children=[
                inputs,
                html.Div(
                    className="d-flex flex-column flex-fill overflow-hidden",
                    children=[
                        html.Div(id=ids.DESC_HIKE, children=[]),
                        profile_graph,
                        html.Div(
                            className="d-flex flex-column flex-fill",
                            children=[loader, map_content],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
