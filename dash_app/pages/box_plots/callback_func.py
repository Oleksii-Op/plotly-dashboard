import plotly.express as px
import plotly.graph_objects as go
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


# BOX PLOT
def update_boxplot(
    nps_type: str,
    dataframe: "pd.DataFrame",
) -> go.Figure:
    nps_df, months, months_names = dataframe.all_nps_prices

    months = months[12:]

    fig = go.Figure()
    for index, date in enumerate(months):
        fig.add_trace(
            go.Box(
                y=nps_df[nps_type].loc[date],
                name=str(months_names[index]),
                boxpoints="outliers",
                boxmean=True,
            )
        )

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            zeroline=True,
            showticklabels=True,
        ),
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            gridcolor="rgb(50, 50, 255)",
            dtick=100,
            gridwidth=1,
            zerolinewidth=2,
        ),
        height=800,
        width=850,
        title_text=f"Boxplot {nps_type} prices for 2023",
    )

    return fig


# HISTOGRAM PLOT
def update_histogram(
    nps_type: str,
    slider: int,
    log_y: str,
    dataframe: "pd.DataFrame",
) -> go.Figure:
    log_y = True if log_y == "True" else False
    nps_df, months, months_names = dataframe.all_nps_prices

    fig2 = px.histogram(
        nps_df["2023-01-01":"2023-12-31"],
        x=nps_type,
        nbins=slider,
        log_y=log_y,
        height=700,
        width=700,
        facet_col_spacing=0.1,
        marginal="violin",
        color_discrete_sequence=px.colors.qualitative.Prism,
    )

    fig2.update_layout(
        yaxis_title="Count number",
        title=f"<b>Price distribution for {nps_type}<b>",
        xaxis_title=nps_type,
        bargap=0.2,
    )

    fig2.update_traces(
        hovertemplate="<b>Price range = %{x}</b><br>Count = %{y}",
    )

    return fig2


# def update_graph(
#     nps_type: str,
#     slider: int,
#     log_y: bool,
#     dataframe: "pd.DataFrame",
# ) -> tuple[
#     go.Figure,
#     px.histogram,
#     str,
# ]:
#     log_y = True if log_y == "True" else False
#     nps_df, months, months_names = dataframe.all_nps_prices
#
#     months = months[12:]
#
#     fig = go.Figure()
#     for index, date in enumerate(months):
#         fig.add_trace(
#             go.Box(
#                 y=nps_df[nps_type].loc[date],
#                 name=str(months_names[index]),
#                 boxpoints="outliers",
#                 boxmean=True,
#             )
#         )
#
#     fig2 = px.histogram(
#         nps_df["2023-01-01":"2023-12-31"],
#         x=nps_type,
#         nbins=slider,
#         log_y=log_y,
#         height=700,
#         width=700,
#         facet_col_spacing=0.1,
#         marginal="violin",
#         color_discrete_sequence=px.colors.qualitative.Prism,
#     )
#
#     fig2.update_layout(
#         yaxis_title="Count number",
#         title=f"<b>Price distribution for {nps_type}<b>",
#         xaxis_title=nps_type,
#         bargap=0.2,
#     )
#
#     fig2.update_traces(hovertemplate="<b>Price range = %{x}</b><br>Count = %{y}")
#
#     fig.update_layout(
#         xaxis=dict(showgrid=False, zeroline=True, showticklabels=True),
#         yaxis=dict(
#             autorange=True,
#             showgrid=True,
#             zeroline=True,
#             gridcolor="rgb(50, 50, 255)",
#             dtick=100,
#             gridwidth=1,
#             zerolinewidth=2,
#         ),
#         height=800,
#         width=850,
#         title_text=f"Boxplot {nps_type} prices for 2023",
#     )
#
#     return fig, fig2, f"You have selected: {slider} bins"
