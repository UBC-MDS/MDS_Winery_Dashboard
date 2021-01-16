
import dash
import dash_html_components as html
import dash_core_components as dcc
import altair as alt
import pandas as pd
#from vega_datasets import data

alt.data_transformers.disable_max_rows()
data = pd.read_csv('data/raw/wine_review.csv')
filtered = data.query('country == "US" & province == "Oregon"') 

def plot_altair():
    chart = alt.Chart(filtered, title = 'Wine Rating by Price ').mark_circle().encode(
        x = 'price',
        y = alt.Y('points', scale=alt.Scale(zero=False)))
    return chart.to_html()

app = dash.Dash(__name__ , external_stylesheets=['https://codepen.io/chriddyp/pen/dZVMbK.css'])
app.layout = html.Div([
    html.H1('App Layout for DSCI_531'),
    dcc.Dropdown(
        options=[
            {'label' : 'Canada', 'value' : 'Canada'},
            {'label': 'United States', 'value' : 'US'}],
            placeholder='Select a Country', multi=True
    ),
     dcc.Dropdown(
        options=[
            {'label' : 'Washington', 'value' : 'Washington'},
            {'label': 'Oregon', 'value' : 'Oregon'}],
            placeholder='Select a State', multi=True
    ),
    dcc.Dropdown(
        options=[
            {'label' : 'Red', 'value' : 'Red'},
            {'label': 'White', 'value' : 'White'}],
            placeholder='Select a Variety', multi=True
    ),
    # dcc.Input(id='widget-1'),
    # html.Div(id='widget-2'),
    html.P('Select your price range'),
    dcc.RangeSlider(min=0, max=200, value=[10,100], marks = {0: '0', 200: '200'}),
    html.P('Select your points range'),
    dcc.RangeSlider(min=80, max=100, value=[85, 90], marks = {80: '80', 100: '100'}),
    html.Iframe(srcDoc=plot_altair(),
            style={'border-width': '0', 'width': '100%', 'height': '400px'})
            ])


# from dash.dependencies import Input, Output
# @app.callback(
#     Output('widget-2', 'children'),
#     Input('widget-1', 'value'))
# def update_output(input_value):
#     return input_value


app.run_server(debug=True) 