from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import callback, Output, Input
from .callback_func import update_boxplot, update_histogram
from dash_app.core.dataframes import data as dataframe


nps_buttons = [
    ["NPS Estonia", "NPS Estonia", "blue"],
    ["NPS Latvia", "NPS Latvia", "orange"],
    ["NPS Lithuania", "NPS Lithuania", "red"],
    ["NPS Finland", "NPS Finland", "green"],
]


header = html.H4(
    children=f"NPS Prices Boxplot and Prices Distribution Histogram for 2023",
    style={"textAlign": "center"},
    className="bg-primary text-white p-2 mb-2 text-center",
)

nps_type_button_selector = html.Div(
    [
        dmc.RadioGroup(
            [dmc.Radio(l, value=k, color=c) for k, l, c in nps_buttons],
            value="NPS Estonia",
            size="md",
            id="radio-nps",
        )
    ],
    style={
        "width": "150%",
        "display": "inline-block",
    },
)

logy_button_selector = html.Div(
    [
        dmc.Text(
            "Enable Log on Y-axis",
            color="blue",
            weight=700,
        ),
        dmc.RadioGroup(
            [
                dmc.Radio(l, value=k, color=c)
                for k, l, c in [
                    ["True", "On", "red"],
                    ["False", "Off", "blue"],
                ]
            ],
            value="False",
            size="md",
            id="log-y-axis",
        ),
    ],
)

# Box plot figure
displayed_boxplot = html.Div(
    [dcc.Graph(figure={}, id="boxplot-graph")],
    style={
        "width": "50%",
        "display": "inline-block",
        "padding": "0 20",
    },
)

displayed_histogram = dcc.Graph(
    figure={},
    id="price-histogram",
)

histogram_slider = dmc.Slider(
    id="drag-slider",
    value=26,
    updatemode="drag",
    marks=[
        {"value": 20, "label": "20 bins"},
        {"value": 50, "label": "50 bins"},
        {"value": 80, "label": "80 bins"},
    ],
)

layout = html.Div(
    [
        header,
        html.Hr(),
        html.Div(
            [
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(
                            nps_type_button_selector,
                            color="info",
                            style={"left": "4%"},
                        ),
                        dbc.ListGroupItem(
                            logy_button_selector,
                            color="info",
                            style={"left": "30%"},
                        ),
                    ],
                    horizontal=True,
                ),
            ]
        ),
        html.Hr(),
        displayed_boxplot,
        html.Div(
            [
                displayed_histogram,
                histogram_slider,
                dmc.Space(h=35),
                dmc.Text(id="drag-output"),
            ],
            style={
                "display": "inline-block",
                "width": "50%",
                "padding": "0 20",
            },
        ),
    ]
)


@callback(
    Output("boxplot-graph", "figure"),
    Input("radio-nps", "value"),
)
def update_boxplot_graph(nps_type: str):
    return update_boxplot(
        nps_type=nps_type,
        dataframe=dataframe,
    )


@callback(
    Output("price-histogram", "figure"),
    Input("radio-nps", "value"),
    Input("log-y-axis", "value"),
    Input("drag-slider", "value"),
)
def update_histogram_graph(
    nps_type: str,
    logy_axis: str,
    drag_slider: int,
):
    return update_histogram(
        nps_type=nps_type,
        log_y=logy_axis,
        slider=drag_slider,
        dataframe=dataframe,
    )


@callback(
    Output("drag-output", "children"),
    Input("drag-slider", "value"),
)
def update_slider_output(slider_value: int) -> str:
    return f"You have selected: {slider_value} bins"
