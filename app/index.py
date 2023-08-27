from layout import layout
from app import app
from callbacks import display_itinerary, export, hike_track, modal, search_itinerary, update_data, update_figure

app.layout = layout
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)