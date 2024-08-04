import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


# PIE CHART
def update_graph(
    year: str,
    data: "pd.DataFrame",
) -> go.Figure:
    total_gw, total_fos_ren = data.total_prod_by_year(year)
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[
            [
                {"type": "domain"},
                {
                    "type": "domain",
                },
            ]
        ],
        subplot_titles=("<b>All types<b>", "<b>Fossil and Renewable<b>"),
    )

    fig.add_trace(
        go.Pie(
            values=total_gw["Production"].values,
            labels=total_gw.index,
            hole=0.3,
            marker=dict(
                colors=px.colors.sequential.thermal_r,
            ),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Pie(
            values=total_fos_ren[f"{year}-12-31"].values,
            labels=total_fos_ren.index,
            hole=0.3,
            marker=dict(colors=["#8C564B", "#00CC96"]),
        ),
        row=1,
        col=2,
    )

    fig.update_layout(
        title_text=f"<b>Total Power Production in {year} in Estonia (GigaWatts)<b>",
        height=1000,
        width=1200,
        showlegend=False,
    )
    fig.update_traces(
        hoverinfo="label+percent+value",
        textinfo="label+percent",
        textfont_size=10,
    )

    return fig
