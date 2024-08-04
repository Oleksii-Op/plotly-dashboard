import plotly.express as px
from dash import html
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm
from scipy.stats import pearsonr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


corr_methods = [
    ["pearson", "Pearson", "blue"],
    ["spearman", "Spearman", "orange"],
    ["kendall", "Kendall", "red"],
]


def correlation_scatter(
    column,
    sample_year,
    resample_by,
    dataframe: "pd.DataFrame",
) -> tuple[go.Figure, html.Div]:
    if sample_year == "All":
        df_weekly = dataframe.power_prod_and_prices.resample(resample_by).mean()
    else:
        df_weekly = (
            dataframe.power_prod_and_prices[
                f"{sample_year}-01-01":f"{sample_year}-12-31"
            ]
            .resample(resample_by)
            .mean()
        )

    X = sm.add_constant(df_weekly[column])
    model = sm.OLS(df_weekly["NPS Estonia"], X).fit()
    coefficients = model.params
    equation = "Y = "
    for i, coeff in enumerate(coefficients):
        if i == 0:
            equation += f"{coeff:.2f}"
        else:
            equation += f" + {coeff:.2f} * {column}"

    collapse = html.Div(
        [
            html.H5(f"Regression (OLS) equation  {equation}"),
            html.Hr(),
            html.H5(f"R^2 = {model.rsquared}"),
            html.Hr(),
            html.H5(f"Correlation = {np.sqrt(model.rsquared)}"),
            html.Hr(),
            html.H5(f"Mean Squared Error (SST) = {model.mse_total}"),
            html.H5(f"Mean Squared Error (SSE) = {model.mse_model}"),
        ]
    )

    y_pred = model.predict(X)

    fig = px.scatter(
        df_weekly,
        x=column,
        y="NPS Estonia",
        trendline="ols",
        trendline_scope="overall",
        height=700,
        title=f"<b>Scatter Plot with Regression line (Ordinary Least Squares!!!) for {sample_year} year/years<b>",
        color=column,
        trendline_color_override="#620042",
    )

    fig.update_layout(showlegend=False)

    # print(model.rsquared, model.mse_model, model.mse_total)

    correlation, p_value = pearsonr(df_weekly[column], df_weekly["NPS Estonia"])
    #
    # print("Correlation coefficient:", correlation)
    # print("p-value:", p_value)

    return fig, collapse


def update_heatmap(
    correlation_method,
    sample_year,
    dataframe: "pd.DataFrame",
) -> go.Figure:
    if sample_year == "All":
        df_corr = dataframe.power_prod_and_prices
    else:
        df_corr = dataframe.power_prod_and_prices[
            f"{sample_year}-01-01":f"{sample_year}-12-31"
        ]
    df_corr = df_corr.corr(
        method=correlation_method,
    )

    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            y=df_corr.columns,
            x=df_corr.index,
            z=np.array(df_corr),
            text=df_corr.values,
            texttemplate="%{text:.2f}",
        )
    )
    fig.update_layout(
        title=f"<b>{correlation_method.capitalize()} Correlation Heatmap for {sample_year} year/years<b>",
        height=700,
    )

    return fig
