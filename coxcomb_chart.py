import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df_medals = pd.read_csv("./Data/Paris Olympic 2024/medals.csv")
disciple = [
    "Wrestling",
    "Athletics",
    "Artistic Gymnastics",
    "Swimming",
    "Weightlifting",
]
top_10_countries = (
    df_medals.groupby("country_code")["country_code"]
    .agg("count")
    .sort_values(ascending=False)
    .head(10)
)

countries = top_10_countries.index.tolist()
data = df_medals[
    df_medals["country_code"].isin(countries) & df_medals["discipline"].isin(disciple)
]

countries_medals = (
    data.groupby(["country_code", "medal_type", "discipline"])["medal_type"]
    .agg("count")
    .reset_index(name="count")
    .sort_values(by=["discipline", "count"], ascending=[True, False])
)

# Update the name of the country in the title
countries_medals["country_code"] = countries_medals["country_code"].replace(
    {
        "USA": "United States",
        "GBR": "Great Britain",
        "KOR": "KOREA",
        "AUS": "Australia",
        "CHN": "China",
        "JPN": "Japan",
        "NED": "Netherlands",
        "GER": "Germany",
        "FRA": "France",
        "ITA": "Italy",
    }
)

# Create a subplot with 2 rows and 5 columns
fig = make_subplots(
    rows=2,
    cols=5,
    specs=[[{"type": "polar"}] * 5] * 2,  # Each subplot is a polar chart
    subplot_titles=[
        f"{country}" for country in countries_medals["country_code"].unique()
    ],
)

# Add each country's polar chart to the subplot
row, col = 1, 1
for i, country in enumerate(countries_medals["country_code"].unique()):
    country_data = countries_medals[countries_medals["country_code"] == country]
    polar_chart = px.bar_polar(
        country_data,
        r="count",
        theta="discipline",
        color="medal_type",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
    )

    # Add the polar chart to the subplot
    for trace in polar_chart.data:
        fig.add_trace(trace, row=row, col=col)

    # Update row and column for the next subplot
    col += 1
    if col > 5:  # Move to the next row after 5 columns
        col = 1
        row += 1

# Update layout
fig.update_layout(
    title_text="PARIS 2024 OLYMPIC GAMES - MEDALS BY DISCIPLINE",
    title_font_color="seashell",  # Set main title font color to white
    title_font_family="Arial",
    title_x=0.5,
    title_font=dict(size=40),  # Increase main title font size
    margin=dict(t=200),  # Increase space between main title and subtitles
    height=1000,  # Adjust height for better spacing
    showlegend=False,  # Hide legend for individual subplots
    plot_bgcolor="firebrick",  # Set the plot background to black
    paper_bgcolor="black",  # Set the overall background to black
    font=dict(color="seashell"),  # Set font color to white for better contrast
)

# Adjust spacing and font size of subplot titles
for annotation in fig["layout"]["annotations"]:
    annotation["yanchor"] = "bottom"  # Anchor the title to the bottom
    annotation["y"] += 0.05  # Add vertical space between the title and the chart
    annotation["font"] = dict(size=20)  # Increase subplot title font size

# Show the figure
fig.show()
fig.write_image(
    "coxcomb_chart_high_res.png", width=2000, height=1000, scale=2
)  # Adjust resolution and scale as needed
