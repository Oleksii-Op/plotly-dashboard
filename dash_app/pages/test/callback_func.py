from dash_app.core.dataframes import data as dataframe
import plotly.express as px
import plotly.graph_objects as go


df = dataframe.production_nps

# def show_static_plot():
loc = (
    df[["NPS Estonia", "Biomass", "Fossil Oil shale"]]
    .loc["2022-05-01":"2022-06-01"]
    .resample("6H")
    .mean()
)

fig = go.Figure(
    px.line(
        loc,
        x=loc.index,
        y=loc.columns,
        title="Common patterns for Prices, Biomass and Fossil Oil shale May 2022",
        height=800,
        width=1000,
    )
)
fig.update_xaxes(
    dtick="%b %d",
    tickformat="%d %B %Y",
    ticklabelmode="period",
)

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(),
        rangeslider=dict(visible=True),
        type="date",
    )
)
fig.update_yaxes(range=[0, 800])

fig.add_annotation(
    x="2022-05-24",
    y=701.3333,
    xref="x",
    yref="y",
    text="Common patterns",
    showarrow=True,
    font=dict(
        family="Courier New, monospace",
        size=16,
        color="#ffffff",
    ),
    align="center",
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#636363",
    ax=20,
    ay=-30,
    bordercolor="#c7c7c7",
    borderwidth=2,
    borderpad=4,
    bgcolor="#ff7f0e",
    opacity=0.8,
)

fig.add_annotation(
    x="2022-05-05",
    y=517,
    xref="x",
    yref="y",
    text="Common patterns",
    showarrow=True,
    font=dict(
        family="Courier New, monospace",
        size=16,
        color="#ffffff",
    ),
    align="center",
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#636363",
    ax=20,
    ay=-30,
    bordercolor="#c7c7c7",
    borderwidth=2,
    borderpad=4,
    bgcolor="#ff7f0e",
    opacity=0.8,
)

fig.update_layout(
    yaxis_title="MW or €/MW/h)",
    xaxis_title="Dates",
    legend_title="Types and Price",
)

fig.update_traces(
    hovertemplate="<b>%{x}</b><br>Production/Price=%{y}",
)

fig.add_vrect(
    x0="2022-05-17",
    x1="2022-06-01",
    line_width=0,
    fillcolor="red",
    opacity=0.2,
)
fig.add_vrect(
    x0="2022-05-03",
    x1="2022-05-06",
    line_width=0,
    fillcolor="red",
    opacity=0.2,
)

fig.show()
