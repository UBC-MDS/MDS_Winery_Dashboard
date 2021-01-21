import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd

alt.data_transformers.disable_max_rows()
df = pd.read_csv('../data/processed/cleaned_data.csv')
df = df.query('country == "US" ') 

# Setup app and layout/frontend
app = dash.Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    html.Iframe(
        id='map',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    html.Label(['province Selection']),
    dcc.Dropdown(
        id='province-widget',
        value='Select your province',  # REQUIRED to show the plot on the first page load
        options=[{'label': province, 'value': province} for province in df['state'].unique()]),
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
    Output('map', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def plot_altair(selected_province, price_value, points_value):
    if selected_province == 'Select your province':
        df_filtered = df
    else:
        df_filtered = df[df['state'] == selected_province]

    state_map = alt.topo_feature(data.us_10m.url, 'states')
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    states_grouped = df_filtered.groupby(['state', 'state_id'], as_index=False)
    wine_states = states_grouped.agg({'points': ['mean'],
                                      'price': ['mean'],
                                      'value': ['mean'],
                                      'description': ['count']})

    wine_states.columns = wine_states.columns.droplevel(level=1)
    wine_states = wine_states.rename(columns={"state": "State",
                                              "state_id": "State ID",
                                              "description": "Num Reviews",
                                              "points": 'Ave Rating',
                                              "price": 'Ave Price',
                                              "value": 'Ave Value'})
    map_click = alt.selection_multi(fields=['state'])
    states = alt.topo_feature(data.us_10m.url, "states")

    colormap = alt.Scale(domain=[0, 100, 1000, 2000, 4000, 8000, 16000, 32000],
                         range=['#C7DBEA', '#CCCCFF', '#B8AED2', '#3A41C61',
                                '#9980D4', '#722CB7', '#663399', '#512888'])

    foreground = alt.Chart(states).mark_geoshape().encode(
        color=alt.Color('Num Reviews:Q',
                        scale=colormap),

        tooltip=[alt.Tooltip('State:O'),
                 alt.Tooltip('Ave Rating:Q', format='.2f'),
                 alt.Tooltip('Ave Price:Q', format='$.2f'),
                 alt.Tooltip('Ave Value:Q', format='.2f'),
                 alt.Tooltip('Num Reviews:Q')]
    ).mark_geoshape(
        stroke='black',
        strokeWidth=0.5
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(wine_states,
                             'State ID',
                             ['State', 'State ID', 'Ave Rating', 'Ave Price', 'Ave Value', 'Num Reviews'])
    ).project(
        type='albersUsa'
    )

    background = alt.Chart(states).mark_geoshape(
        fill='gray',
        stroke='dimgray'
    ).project(
        'albersUsa'
    )
    chart = (background + foreground).configure_view(
                height=400,
                width=570,
                strokeWidth=4,
                fill=None,
                stroke=None).encode(opacity=alt.condition(map_click, alt.value(1), alt.value(0.2))).add_selection(map_click)
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)