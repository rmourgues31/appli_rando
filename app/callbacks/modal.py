from dash import Input, Output, State
from components import ids
from app import app

for (modal_id,open_id, close_id) in [
    (ids.MODAL_AGENCIES, ids.OPEN_AGENCIES, ids.CLOSE_AGENCIES),
    (ids.MODAL_CREDITS, ids.OPEN_CREDITS,ids.CLOSE_CREDITS),
    (ids.MODAL_TUTORIAL, ids.OPEN_TUTORIAL, ids.CLOSE_TUTORIAL),
    (ids.MODAL_EXAMPLES, ids.OPEN_EXAMPLES, ids.CLOSE_EXAMPLES)]:
    def toggle_modal(n1: int, n2: int, is_open: bool) -> bool:
        if n1 or n2:
            return not is_open
        return is_open
    app.callback(
        Output(modal_id, "is_open"),
        [Input(open_id, "n_clicks"), Input(close_id, "n_clicks")],
        [State(modal_id, "is_open")],
    )(toggle_modal)
