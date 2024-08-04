from datetime import date
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash_app.core.dataframes import data as dataframe
import dash_mantine_components as dmc
from .callback_func import update_graph


layout = html.Div(
    [
        html.H4(
            children=f"Comparing NPS Prices - Line plots",
            style={"textAlign": "center"},
            className="bg-primary text-white p-2 mb-2 text-center",
        ),
        html.Hr(),
        html.Div(
            [
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(
                            html.Div(
                                [
                                    dmc.MultiSelect(
                                        label="Select NPS you like!",
                                        placeholder="Select all NPS you like!",
                                        id="nps-dropdown",
                                        value=["NPS Estonia"],
                                        data=[
                                            "NPS Estonia",
                                            "NPS Latvia",
                                            "NPS Lithuania",
                                            "NPS Finland",
                                        ],
                                        style={"width": 600, "height": 100},
                                    )
                                ]
                            )
                        ),
                        dbc.ListGroupItem(
                            html.Div(
                                [
                                    dmc.DateRangePicker(
                                        id="date-range-picker-nps",
                                        label="Date Range",
                                        description="Select a range",
                                        minDate=date(2022, 1, 1),
                                        maxDate=date(2023, 12, 31),
                                        amountOfMonths=2,
                                        value=[
                                            date(2022, 1, 1),
                                            date(2023, 12, 31),
                                        ],
                                        style={"width": 330, "height": 100},
                                    ),
                                    dmc.Space(h=10),
                                    dmc.Text(id="selected-date-date-range-picker"),
                                ]
                            )
                        ),
                        dbc.ListGroupItem(
                            html.Div(
                                [
                                    dmc.Text(
                                        "Mean/Median sample",
                                        color="blue",
                                        weight=700,
                                    ),
                                    dmc.RadioGroup(
                                        [
                                            dmc.Radio(l, value=k, color=c)
                                            for k, l, c in [
                                                ["median", "Median", "red"],
                                                ["mean", "Mean", "blue"],
                                            ]
                                        ],
                                        value="mean",
                                        size="md",
                                        id="median-mean",
                                        style={"width": 200, "height": 100},
                                    ),
                                ],
                                style={
                                    "width": "100%",
                                },
                            )
                        ),
                        dbc.ListGroupItem(
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
                                            {
                                                "label": "12 Hours",
                                                "value": "12h",
                                            },
                                            {"label": "1 Day", "value": "1d"},
                                            {"label": "2 Days", "value": "2d"},
                                            {"label": "3 Days", "value": "3d"},
                                            {"label": "4 Days", "value": "4d"},
                                            {"label": "5 Days", "value": "5d"},
                                        ],
                                        id="sampling-prices",
                                        value="5d",
                                    ),
                                ],
                                style={"width": 150, "height": 100},
                            )
                        ),
                    ],
                    horizontal=True,
                )
            ],
            style={
                "width": "30%",
                "display": "inline-block",
                "padding": "0 30",
            },
        ),
        dcc.Graph(figure={}, id="nps-lines"),
    ]
)


@callback(
    Output("nps-lines", "figure"),
    Output("selected-date-date-range-picker", "children"),
    Input("nps-dropdown", "value"),
    Input("median-mean", "value"),
    Input("sampling-prices", "value"),
    Input("date-range-picker-nps", "value"),
)
def update_plot(
    line_prices,
    median_mean,
    resampled_by,
    date_select,
):
    return update_graph(
        line_prices=line_prices,
        median_mean=median_mean,
        date_select=date_select,
        resampled_by=resampled_by,
        dataframe=dataframe,
    )
