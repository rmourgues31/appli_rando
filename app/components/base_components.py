from dash import html, dcc, get_asset_url
import dash_bootstrap_components as dbc
from datetime import date

def render_input(placeholder: str, value: str, id: str) -> dcc.Input:
    '''
    Input component
    '''
    return dcc.Input(id=id, 
              placeholder = placeholder, 
              value=value,
              style={
                'width': '120px',
                'height': '45px',
                'display': 'inline-block','verticalAlign': 'top'
            })

def render_upload(id: str) -> dcc.Upload:
    '''
    Upload drag and drop / open file search
    '''
    return dcc.Upload(
            id=id,
            children=html.Div([
                'Déposer un fichier GPX ou ',
                html.A('Cliquer pour ouvrir l\'explorateur')
            ]),
            # Allow multiple files to be uploaded
            multiple=False,
            style={
                'width': '80%',
                #'height': '30%',
                'lineHeight': '200%',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                #'margin': '10px'
            }
        )
    
def render_datepicker(id: str) -> dcc.DatePickerSingle:
    '''
    Datepicker with default date Today and French format
    '''
    return dcc.DatePickerSingle(
                    id=id,
                    min_date_allowed=date.today(),
                    max_date_allowed=date(2024, 9, 19),
                    initial_visible_month=date.today(),
                    date=date.today(),
                    month_format="DD/MM/YYYY",
                    display_format="DD/MM/YYYY",
                    first_day_of_week=1
                )

def render_dropdown(id: str, options: list[dict], value: str) -> dcc.Dropdown:
    ''''
    Dropdown
    Parameters
        options: [{label:value}]
        value: option to display
    '''
    return dcc.Dropdown(options=options,
                        id=id, 
                        value=value,
                        clearable=True
                        #style={'width': '60%','display': 'inline-block','verticalAlign': 'top'}
                    )

def render_button(id: str, text: str, n_clicks: int = 0) -> dbc.Button:
    '''
    Button
    Parameters
        n_clicks should be equal to -1 if you want to avoid first click at creation
    '''
    return dbc.Button(text, id=id, n_clicks=n_clicks)

def render_modal(title: str, content, id: str, close_id: str, open_id: str, size: str = "xl") -> dbc.Col:
    '''
    Modal with title, content and id
    '''
    return dbc.Col(dbc.NavItem([
            render_button(id=open_id, text=title),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(title)),
                dbc.ModalBody(html.Div(content)),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fermer", id=close_id, className="ms-auto", n_clicks=0
                    )
                )
                ],
                centered=True,
                id=id,
                is_open=False,
                size=size
            )
        ]))

def render_card(content) -> dbc.Card:
    return dbc.Card(dbc.CardBody(content))

def render_icon(url, anchor_x):
        size = 25
        return {
            "iconUrl": get_asset_url(f'icons/{url}'),
            #"shadowUrl": 'https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
            "iconSize": [size, size],  # size of the icon
            #"shadowSize": [50, 64],  # size of the shadow
            "iconAnchor": [anchor_x*size, size],  # point of the icon which will correspond to marker's location
            #"shadowAnchor": [4, 62],  # the same for the shadow
            #"popupAnchor": [-3, -76]  # point from which the popup should open relative to the iconAnchor
        }