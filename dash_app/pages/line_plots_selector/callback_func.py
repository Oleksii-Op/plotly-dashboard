import plotly.express as px
import plotly.graph_objects as go
from typing import TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    import pandas as pd


def update_graph(
    line_prices,
    median_mean,
    resampled_by,
    date_select,
    dataframe: "pd.DataFrame",
):
    if not line_prices:
        line_prices = ["Estonia"]
    parsed_dates = []
    print(date_select)
    if date_select is None:
        date_select = ["2022-01-01", "2023-12-31"]
    print(date_select)
    for date_str in date_select:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        parsed_dates.append(parsed_date)

    start, end = parsed_dates

    # date_start = datetime.strptime(start, '%Y-%m-%d').strftime('%Y-%m-%d')
    # date_end = datetime.strptime(end, '%Y-%m-%d').strftime('%Y-%m-%d')

    df_weekly, _, _ = dataframe.all_nps_prices
    df_weekly = df_weekly[str(start) : str(end)]
    if median_mean == "mean":
        df_weekly = df_weekly.resample(resampled_by).mean()
    else:
        df_weekly = df_weekly.resample(resampled_by).median()
    fig = go.Figure(
        px.line(
            df_weekly,
            x=df_weekly.index,
            y=df_weekly[line_prices].columns,
            title="<b>Nord Pole prices for 2022 and 2023<b>",
            height=900,
        )
    )
    # fig.update_xaxes(
    #     dtick="M1",
    #     tickformat="%d %B %Y",
    #     ticklabelmode="period")

    fig.update_layout(
        yaxis_title="<b>Price EUR / MWh<b>",
        xaxis_title="<b>Dates<b>",
        legend_title="<b>Price<b>",
    )

    fig.update_traces(hovertemplate="<b>%{x}</b><br>Price=%{y} <b>EUR / MWh<b>")
    prefix = "You have selected: "
    text_varchar = prefix + "   -   ".join([str(start), str(end)])

    return fig, text_varchar
