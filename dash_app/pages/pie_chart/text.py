from dash import html

body = [
    html.P(
        """In comparison to electricity production from renewable and fossil 
                fuels in 2022 and 2023, there was a significant reliance on Fossil
                oil shale in 2022, accounting for 57.9% of all electricity types."""
    ),
    html.Hr(),
    html.P(
        """In 2023, it decreased to 43.2%. Looking at the pie chart of fossil
                and renewable electricity types, we see that fossil fuels comprised
                65.3% and renewables 34.7% in 2022. In 2023, renewable energy increased
                to 43.3%, while fossil fuels decreased to 56.7%. Additionally, biomass
                ranked second in 2022 but was replaced by wind power in 2023.
                Wind energy moved to third place in 2023, with solar energy taking its spot.
                But, I have to note that the production in MW decreased too compared to 2022."""
    ),
    html.Hr(),
    html.H5(
        """Overall, the percentage of Fossil oil shale noticeably decreased.
                From 57.9% before the 2022, it dropped to 43.2% in 2023,
                indicating a less reliance on fossil energy sources and steps towards renewable energy sources."""
    ),
]
