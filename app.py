import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample data
df = pd.read_csv('./Data/Paris Olympic 2024/medals_total.csv')
df.sort_values(by='Total', ascending=False, inplace=True)
# Select the top 10 countries
df = df.head(10)

# Create a Dash app
app = dash.Dash(__name__)



fig = px.bar(df, x="country_code", y="Total", title="Sample Bar Chart")

# Define the app layout
app.layout = html.Div([
    html.H1("Dash with Plotly Visualization"),
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == "__main__":
    print("App is running...")
    app.run(debug=True)  # Updated method