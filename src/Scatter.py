import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd

alt.data_transformers.disable_max_rows()
df = pd.read_csv('data/raw/wine_data.csv')
df = df.query('country == "US" ') 

# Setup app and layout/frontend
app = dash.Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    html.Label(['province Selection']),
    dcc.Dropdown(
        id='province-widget',
        value='Oregon',  # REQUIRED to show the plot on the first page load
        options=[{'label': province, 'value': province} for province in df['province'].unique()]),
    html.Br(),
    html.Label(['Price Range']),
    dcc.RangeSlider(
        id='price',
        min=df['price'].min(),
        max=df['price'].max(),
        value=[df['price'].min(), df['price'].max()]),
    html.Br(),
    html.Label(['Point Range']),
    dcc.RangeSlider(
        id='points',
        min=df['points'].min(),
        max=df['points'].max(),
        value=[df['points'].min(), df['points'].max()])])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def plot_altair(selected_province, price_value, points_value):
    df_filtered = df[df['province'] == selected_province]
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    chart = alt.Chart(df_filtered).mark_point().encode(
        x=alt.X('price', scale=alt.Scale(zero=False)),
        y=alt.Y('points', scale=alt.Scale(zero=False)),
        color = 'variety',
        tooltip='variety').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)