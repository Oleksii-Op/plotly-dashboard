from dash import html
from dash_mantine_components import Alert

text = """
        This interactive dash board was created as a part 
        of my Data Science internship test task.
        
        The main purpose of this dash board is to give full 
        freedom to interact with plots using date selectors, 
        buttons, different correlation methods and resampling.
        
         
        """

layout = html.Div(
    [
        html.H1("Welcome"),
        html.Hr(),
        html.H5(
            """
        This interactive dash board was created as a part 
        of my Data Science internship test task."""
        ),
        html.Hr(),
        html.H5(
            """
        The main purpose of this dash board is to give full 
        freedom to interact with plots using date selectors, 
        buttons, different correlation methods and resampling.
        """
        ),
        html.Hr(),
        html.H5(
            """
            The dataset provided with this task contains a wealth of 
            information about energy production and power market 
            prices that can provide valuable insights into production
            trends and pricing patterns.
        """
        ),
        html.Hr(),
        html.H5(
            """
            The dataset has 2 files named est_power_production_2022-2023.csv 
            and nps_2022_2023.csv which are used in the LoadDataFrame class that 
            feeds all the plots in this dash application.
        """
        ),
        html.Hr(),
        Alert(
            "Please note that this dashboard is not yet finished!",
            title="Warning!",
            color="red",
            radius="xl",
        ),
    ],
    style={
        "textAlign": "left",
        "padding": "20px",
        "border": "2px solid powderblue",
        "width": "40%",
    },
)
