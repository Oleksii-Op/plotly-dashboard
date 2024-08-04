from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import callback, Output, Input
from .callback_funcs import update_area, update_lines
from dash_app.core.dataframes import data as dataframe


header = html.H4(
    children=f"Total Power Production 2022 and 2023",
    style={"textAlign": "center"},
    className="bg-primary text-white p-2 mb-2 text-center",
)

year_selector = html.Div(
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
            id="year-selector",
        ),
    ]
)

displayed_plots = html.Div(
    [
        dcc.Graph(figure={}, id="foss_renew"),
        dcc.Graph(figure={}, id="line-all-types"),
    ],
    style={
        "display": "inline-block",
        "width": "50%",
        "padding": "0 0",
    },
)

layout = html.Div(
    [
        header,
        dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    year_selector,
                ),
            ],
            horizontal=True,
            className="mb-2",
        ),
        displayed_plots,
    ]
)


# AREA CHART
@callback(
    Output("foss_renew", "figure"),
    Input("year-selector", "value"),
)
def update_area_chart(year: str):
    return update_area(
        year=year,
        data=dataframe,
    )


# LINE GRAPH
@callback(
    Output("line-all-types", "figure"),
    Input("year-selector", "value"),
)
def update_line_chart(year: str):
    return update_lines(
        year=year,
        data=dataframe,
    )
