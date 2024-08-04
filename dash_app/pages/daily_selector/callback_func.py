from datetime import datetime
import plotly.express as px
from dash import no_update
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
    import plotly.graph_objs as go


# BAR PLOT
def update_graph(
    date_value: str,
    dataframe: "pd.DataFrame",
) -> "go.Figure":
    if date_value:
        date_value = datetime.strptime(
            date_value,
            "%Y-%m-%d",
        ).strftime("%Y-%m-%d")
        dff = dataframe.power_production[date_value:date_value]
        my_bar = px.bar(
            dff,
            y=dff.columns,
            x=dff.index,
            height=1000,
            color_discrete_sequence=px.colors.qualitative.Prism,
        )

        my_bar.update_layout(
            # title="Daily Energy Production types bars for 2022-2023",
            xaxis_title="Hours",
            yaxis_title="Production (MW)",
            xaxis_visible=True,
            legend_title="Energy production types",
        )

        my_bar.update_traces(
            hovertemplate="<b>%{x}</b><br>Production - %{y} MW",
        )

        return my_bar
    else:
        no_update()
