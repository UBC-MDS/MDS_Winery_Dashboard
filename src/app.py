import dash
import dash_html_components as html
import dash_core_components as dcc
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from vega_datasets import data

alt.data_transformers.disable_max_rows()
df = pd.read_csv('/Users/neelphaterpekar/Desktop/MDS/MDS_Block4/DSCI_532/group_6/data/raw/wine_data.csv') # data/raw/wine_data.csv
df = df.query('country == "US"') 
#filtered = data

# @app.callback(
#     Output('widget-2', 'children'),
#     Input('widget-1', 'value'))
# def update_output(input_value):
#     return input_value
def plot_map():
    counties = alt.topo_feature(data.us_10m.url, 'counties')
    source = data.unemployment.url
    chart= alt.Chart(counties).mark_geoshape().encode(
    color='rate:Q'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(source, 'id', ['rate'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300
)

    return chart.to_html()
    
app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab( label='Winary Dashboard'),
        dcc.Tab( label='Data')]),
    html.H1('MDS Winary Dashboard'),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Label([
                'Country Selection']),
            dcc.Dropdown(
                options=[{'label': country, 'value': country} for country in df['country'].unique()],
                placeholder='Select a Country', 
                multi=True
            ),
            html.Label([
                'Provice/State Selection']),
            dcc.Dropdown(
                id='province-widget',
                value='Oregon', 
                options=[{'label': province, 'value': province} for province in df['province'].unique()],
                placeholder='Select a State'
            ),
            html.Label(['Wine Type']
            ),
            dcc.Dropdown(
                id='wine_variety',
                value='Red Blend', 
                options=[{'label': variety, 'value': variety} for variety in df['variety'].unique()],
                placeholder='Select a Variety', 
                multi=True
            ),
            html.Br(),
            html.Label(['Price Range']
            ),
            dcc.RangeSlider(
                id='price',
                min=df['price'].min(),
                max=df['price'].max(),
                value=[df['price'].min(), df['price'].max()]
            ),
            html.Label(['Points Range']
            ),
            dcc.RangeSlider(
                id='points',
                min=df['points'].min(),
                max=df['points'].max(),
                value=[df['points'].min(), df['points'].max()]
                ),
            html.Label(['Value Ratio']
            ),
            dcc.RangeSlider(min=0, max=1, step=0.1, value=[0.2,0.6], marks = {0: '0', 0.2: '0.2', 0.4: '0.4', 0.6: '0.6', 0.8: '0.8', 1: '1'}  
            ),
            ], md=5, style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),
        dbc.Col([
            html.Iframe(srcDoc=plot_map(),
                style={'border-width': '0', 'width': '100%', 'height': '400px'})
            ], md=7)
        ]),
        dbc.Row([
        dbc.Col([
            html.Iframe(
                id = 'plots',
                style={'border-width': '0', 'width': '100%', 'height': '700px'})
            ], md=8),
        dbc.Col([
            dbc.Row([
               html.Br(),
               html.Label(['This will be for values in one of the cards'], 
                    style={'border': '1px solid #d3d3d3', 'border-radius': '30px'}),
               html.Br()
            ]),
            html.Br(),
            html.Br(),              # Random spacing added to make the layout more realistic... we should delete at some point 
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
               html.Br(),
               html.Label(['This will be for values in one of the cards'], 
                    style={'border': '1px solid #d3d3d3', 'border-radius': '30px'}),
               html.Br()
            ])
        ])
    ]),
    html.Br(),
    html.Br()
])

@app.callback(
    Output('plots', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'),
    Input('wine_variety', 'value'))
def plot_altair(selected_province, price_value, points_value, wine_variety):
    df_filtered = df[df['province'] == selected_province]
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    df_filtered = df_filtered.query("variety == @wine_variety")
    chart1 = alt.Chart(df_filtered).mark_point().encode(
        x=alt.X('price', scale=alt.Scale(zero=False)),
        y=alt.Y('points', scale=alt.Scale(zero=False)),
        color = 'variety',
        tooltip='variety').interactive()
    
    chart2 = alt.Chart(df_filtered, title = 'Average Price of Selection').mark_bar().encode(
        y = alt.Y('price',title='Average Price ($)'),
        x = alt.X('variety', scale=alt.Scale(zero=False))
    )

    chart = chart1 | chart2
    return chart.to_html()

app.run_server(debug=True)

