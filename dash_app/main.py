import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
from pages.pie_chart.layout import layout as pie_layout
from pages.area_and_line_plots.layout import layout as area_and_line_plots_layout
from pages.daily_selector.layout import layout as daily_selector_layout
from pages.box_plots.layout import layout as box_plots_layout
from pages.line_plots_selector.layout import layout as line_plots_selector_layout
from pages.heatmap.layout import layout as heatmap_layout
from core.config import settings
from dash_app.text_data.home_page_text import text as text_home_page_text
from dash_app.text_data.home_page_text import layout as home_page_layout

app = dash.Dash(
    __name__,
    routing_callback_inputs={
        # The app state is serialised in the URL hash without refreshing the page
        # This URL can be copied and then parsed on page load
        "state": State(
            "main-url",
            "hash",
        ),
    },
    external_stylesheets=[dbc.themes.SPACELAB],
    suppress_callback_exceptions=True,
)

app.config.suppress_callback_exceptions = True

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2(
            "Dash Board",
            className="display-4",
        ),
        html.Hr(),
        html.P(
            "Navigation",
            className="lead",
        ),
        dbc.Nav(
            [
                dbc.NavLink(
                    "Home",
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    "Pie chart",
                    href="/pie-chart",
                    active="exact",
                ),
                dbc.NavLink(
                    "Area/Line",
                    href="/area-line",
                    active="exact",
                ),
                dbc.NavLink(
                    "Date Selector",
                    href="/daily-selector",
                    active="exact",
                ),
                dbc.NavLink(
                    "Box Plots",
                    href="/box-plots",
                    active="exact",
                ),
                dbc.NavLink(
                    "Range Selector",
                    href="/range-selector",
                    active="exact",
                ),
                dbc.NavLink(
                    "Heatmap",
                    href="/heatmap",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    id="page-content",
    style=CONTENT_STYLE,
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        content,
        dash.page_container,
    ]
)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def render_page_content(pathname):
    if pathname == "/":
        return home_page_layout
    elif pathname == "/pie-chart":
        return pie_layout
    elif pathname == "/area-line":
        return area_and_line_plots_layout
    elif pathname == "/daily-selector":
        return daily_selector_layout
    elif pathname == "/box-plots":
        return box_plots_layout
    elif pathname == "/range-selector":
        return line_plots_selector_layout
    elif pathname == "/heatmap":
        return heatmap_layout

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1(
                "404: Not found",
                className="text-danger",
            ),
            html.Hr(),
            html.P(
                f"The pathname {pathname} was not recognised...",
            ),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(
        host=settings.host,
        port=settings.port,
        debug=True,
    )
