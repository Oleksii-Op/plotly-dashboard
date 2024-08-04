from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from .callback_func import (
    update_heatmap,
    correlation_scatter,
)
from dash_app.core.dataframes import data as dataframe


corr_methods = [
    ["pearson", "Pearson", "blue"],
    ["spearman", "Spearman", "orange"],
    ["kendall", "Kendall", "red"],
]

header = html.H4(
    children=f"Correlation and Heatmap",
    style={"textAlign": "center"},
    className="bg-primary text-white p-2 mb-2 text-center",
)

layout = html.Div(
    [
        header,
        html.Div(
            [
                html.Div(
                    [
                        dmc.Text(
                            "Entity to be compared",
                            color="blue",
                            weight=700,
                        ),
                        dcc.Dropdown(
                            dataframe.power_prod_and_prices.columns,
                            id="correlations",
                            value="Solar",
                        ),
                        dmc.Text(
                            "Select a year below",
                            color="blue",
                            weight=700,
                        ),
                        dmc.RadioGroup(
                            [
                                dmc.Radio(l, value=k, color=c)
                                for k, l, c in [
                                    ["2022", "2022", "red"],
                                    ["2023", "2023", "blue"],
                                    ["All", "All", "green"],
                                ]
                            ],
                            value="2022",
                            size="sm",
                            id="sample-year",
                        ),
                    ],
                    style={
                        "width": "49%",
                        "display": "inline-block",
                    },
                ),
                html.Div(
                    [
                        dmc.Text(
                            "Resampling by",
                            color="blue",
                            weight=700,
                        ),
                        dcc.Dropdown(
                            options=[
                                {"label": "1 Hour", "value": "1h"},
                                {"label": "6 Hours", "value": "6h"},
                                {"label": "1 Day", "value": "1d"},
                                {"label": "2 Days", "value": "2d"},
                                {"label": "3 Days", "value": "3d"},
                                {"label": "4 Days", "value": "4d"},
                                {"label": "5 Days", "value": "5d"},
                                {"label": "6 Days", "value": "6d"},
                                {"label": "1 Week", "value": "w"},
                                {"label": "2 Weeks", "value": "2w"},
                                {"label": "3 Weeks", "value": "3w"},
                                {"label": "4 Weeks", "value": "4w"},
                                {"label": "Monthly", "value": "m"},
                            ],
                            id="sampling",
                            value="w",
                        ),
                        dmc.Text(
                            "Correlation methods",
                            color="blue",
                            weight=700,
                        ),
                        dmc.RadioGroup(
                            [
                                dmc.Radio(l, value=k, color=c)
                                for k, l, c in corr_methods
                            ],
                            value="spearman",
                            size="sm",
                            id="correlation-method",
                        ),
                    ],
                    style={
                        "width": "49%",
                        "display": "inline-block",
                    },
                ),
            ],
            style={
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "10px 5px",
            },
        ),
        html.Div(
            [
                dbc.Button(
                    "Regression line info",
                    id="collapse-button",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(children="")),
                    id="collapse",
                    is_open=False,
                ),
            ]
        ),
        html.Div(
            [
                dcc.Graph(
                    figure={},
                    id="correlation-scatter",
                )
            ],
            style={
                "width": "50%",
                "display": "inline-block",
                "padding": "0 20",
            },
        ),
        html.Div(
            [dcc.Graph(figure={}, id="heatmap")],
            style={
                "display": "inline-block",
                "width": "50%",
                "padding": "0 20",
            },
        ),
    ]
)


@callback(
    Output(component_id="correlation-scatter", component_property="figure"),
    Output(component_id="collapse", component_property="children"),
    Input(component_id="correlations", component_property="value"),
    Input(component_id="sample-year", component_property="value"),
    Input(component_id="sampling", component_property="value"),
)
def correlation_scatter_plot(
    column: str,
    sample_year: str,
    resample_by: str,
):
    if not resample_by:
        resample_by = "w"
    if not column:
        column = "Solar"
    return correlation_scatter(
        column=column,
        sample_year=sample_year,
        resample_by=resample_by,
        dataframe=dataframe,
    )


@callback(
    Output(component_id="heatmap", component_property="figure"),
    Input(component_id="correlation-method", component_property="value"),
    Input(component_id="sample-year", component_property="value"),
)
def update_heatmap_plot(
    correlation_method: str,
    sample_year: str,
):
    return update_heatmap(
        correlation_method=correlation_method,
        sample_year=sample_year,
        dataframe=dataframe,
    )


@callback(
    Output("collapse", "is_open"),
    Input("collapse-button", "n_clicks"),
    State("collapse", "is_open"),
)
def toggle_collapse(
    n: int,
    is_open: bool,
) -> bool:
    if n:
        return not is_open
    return is_open
