from dash import html, dcc
from datetime import date
from dash import callback, Output, Input
from .callback_func import update_graph
from dash_app.core.dataframes import data as dataframe

header = html.H4(
    children=f"Daily Energy Production by Types 2022-2023",
    style={"textAlign": "center"},
    className="bg-primary text-white p-2 mb-2 text-center",
)

date_picker = dcc.DatePickerSingle(
    id="my-date-picker",
    min_date_allowed=date(2022, 1, 1),
    max_date_allowed=date(2023, 12, 31),
    initial_visible_month=date(2022, 1, 1),
    date=date(2022, 1, 1),
)

displayed_bar_plot = dcc.Graph(
    figure={},
    id="my-graph-bars",
)

layout = html.Div(
    [
        header,
        date_picker,
        displayed_bar_plot,
    ]
)


@callback(
    Output("my-graph-bars", "figure"),
    Input("my-date-picker", "date"),
)
def update_plot(date_value: str):
    return update_graph(
        date_value=date_value,
        dataframe=dataframe,
    )
