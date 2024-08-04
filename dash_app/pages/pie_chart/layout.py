from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import callback, Output, Input
from .callback import update_graph
from dash_app.core.dataframes import data as dataframe


header = html.H4(
    children=f"Total Power Production 2022 and 2023",
    style={"textAlign": "center"},
    className="bg-primary text-white p-2 mb-2 text-center",
)

year_selector = dbc.ListGroup(
    [
        dbc.ListGroupItem(
            html.Div(
                [
                    dmc.Text(
                        children="Select a year below",
                        color="blue",
                        weight=700,
                    ),
                    dmc.RadioGroup(
                        [
                            dmc.Radio(l, value=k, color=c)
                            for k, l, c in [
                                ["2022", "2022", "red"],
                                ["2023", "2023", "blue"],
                            ]
                        ],
                        value="2022",
                        size="md",
                        id="total-year",
                    ),
                ]
            )
        ),
    ],
    horizontal=True,
    className="mb-2",
)

displayed_plot = html.Div(
    [
        dcc.Graph(
            figure={},
            id="my-graph",
            className="dark-theme-control",
        ),
    ],
    style={
        "width": "50%",
        "display": "inline-block",
        "padding": "0 20",
    },
)

layout = html.Div(
    [
        header,
        year_selector,
        displayed_plot,
    ]
)


@callback(
    Output(component_id="my-graph", component_property="figure"),
    Input("total-year", "value"),
)
def update(year: str):
    return update_graph(
        year=year,
        data=dataframe,
    )
