import plotly.express as px
import plotly.graph_objects as go
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


# AREA PLOT
def update_area(
    year: str,
    data: "pd.DataFrame",
) -> go.Figure:
    fossil_renew_data, prices_trace = data.get_renewables_fossil()
    colors = ["#9D755D", "#66AA00"]

    fig = px.area(
        fossil_renew_data[f"df6_mixed_{year}"],
        x=fossil_renew_data[f"df6_mixed_{year}"].index,
        y=fossil_renew_data[f"df6_mixed_{year}"].columns,
        color_discrete_sequence=colors,
        title=f"<b>Electricity production and spot prices in {year}<b>",
        line_shape="spline",
        height=500,
        width=1300,
    )

    fig.add_trace(
        go.Scatter(
            x=prices_trace[f"{year}"].index,
            y=prices_trace[f"{year}"].values,
            hoverinfo="x+y",
            name="NPS Estonia price",
            line=dict(width=4, color="rgb(204, 80, 62)"),
        )
    )

    fig.update_layout(
        xaxis_title="Months",
        yaxis_title="Production/Price",
        legend_title="<b>Energy production types<b>",
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Production/Price=%{y}",
    )
    return fig


# LINE PLOT
def update_lines(
    year: str,
    data: "pd.DataFrame",
) -> go.Figure:
    dataframe = data.power_production
    df = dataframe[f"{year}-01-01":f"{year}-12-31"].resample("M").mean()

    fig = go.Figure(
        px.line(
            df,
            x=df.index,
            y=df.columns,
            title=f"<b>Energy production by types over {year} resampled by mean monthly<b>",
            height=500,
            width=1300,
            markers=True,
            color_discrete_sequence=px.colors.qualitative.T10,
        )
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period",
    )

    fig.update_layout(
        yaxis_title="Production (MW)",
        legend_title="<b>Energy production types<b>",
        xaxis_title="Dates",
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Production=%{y:.2f} MW",
    )

    fig.update_layout(
        xaxis_rangeslider_visible=False,
    )
    return fig
