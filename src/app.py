import dash
import dash_html_components as html
import dash_core_components as dcc
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from vega_datasets import data

alt.data_transformers.disable_max_rows()

df = pd.read_csv('../data/processed/cleaned_data.csv') #../data/processed/cleaned_data.csv
df = df.query('country == "US" ') 

app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])

server=app.server
"""
Dashboard layout
"""

app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab( label='Winary Dashboard'),
        dcc.Tab( label='Data')]),
    html.H2('MDS Winery Dashboard'),
    dbc.Row([
        dbc.Col([
            html.Br(),
            # html.Label([
            #     'Country Selection']),
            # dcc.Dropdown(
            #     options=[{'label': country, 'value': country} for country in df['country'].unique()],
            #     placeholder='Select a Country', 
            #     multi=True
            # ),
            html.Label([
                'Provice/State Selection']),
            dcc.Dropdown(
                id='province-widget',
                value='select your state',  
                options=[{'label': state, 'value': state} for state in df['state'].unique()],
                placeholder='Select a State',
                # multi=True
            ),
            html.Label(['Wine Type']
            ),
            dcc.Dropdown(
                id='wine_variety',
                value='select a variety', 
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
                value=[df['price'].min(), df['price'].max()],
                marks = {4: '$4', 25: '$25', 50: '$50', 75: '$75', 100: '$100'}
            ),
            html.Label(['Rating Points Range']
            ),
            dcc.RangeSlider(
                id='points',
                min=df['points'].min(),
                max=df['points'].max(),
                value=[df['points'].min(), df['points'].max()],
                marks = {80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}
                ),
            html.Label(['Value Ratio']
            ),
            dcc.RangeSlider(min=0, 
                max=1, 
                step=0.1, 
                value=[0.2,0.6], 
                marks = {0: '0', 0.2: '0.2', 0.4: '0.4', 0.6: '0.6', 0.8: '0.8', 1: '1'}  
            ),
            ], md=4,
            style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),
        dbc.Col([
            html.Iframe(
                id = 'maps',
                style={'border-width': '0', 'width': '100%', 'height': '460px'})
            ], md=8)
        ]),
    dbc.Row([
        dbc.Col([
            html.Iframe(
                id = 'plots',
                style={'border-width': '0', 'width': '100%', 'height': '500px'})
            ], md=8),
        dbc.Col([
            html.Br(),
            dbc.Row([
                html.H4(['Highest Value Wine:']),
                html.Br(),
                html.H5(
                    id = 'highest_value_name'),
                html.Br(),
                html.H3(
                    id = 'highest_value'),
                ], style={'border': '1px solid #d3d3d3', 'padding-left': '22%', 'padding-right': '20%', 'height': '175px', 'border': '1px solid', 'backgroundColor' : '#bfefff'}),  
            html.Br(),    # Random spacing added to make the layout more realistic... we should delete at some point 
            dbc.Row([
                dbc.Col([
                    html.H4(['Highest Wine Score:']),
                    html.Br(),
                    html.H5(
                        id='highest_score_name'),
                    html.H3(
                        id='highest_score'),
                ], style={'border': '1px solid #d3d3d3', 'padding-left': '20%', 'height': '175px', 'border': '1px solid', 'backgroundColor' : '#bfefff'}),
                ])
            ])
        ]),
])

@app.callback(
    Output('highest_score', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'))
def max_score(wine_type, state):
    if state == 'select your state':
        return None
    else:
        df_filtered = df[df['state'] == state]
    if wine_type == 'select a variety':
        return None
    else: 
        df_filtered = df_filtered[df_filtered['variety'] == wine_type]
    max_points = max(df_filtered['points'])
    df_filtered = df[df['points'] == max_points]
    wine_name = df_filtered['title'].iloc[0]

    return str(str(round(max_points,2)))


@app.callback(
    Output('highest_score_name', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'))
def max_score(wine_type, state):
    if state == 'select your state':
        return None
    else:
        df_filtered = df[df['state'] == state]
    if wine_type == 'select a variety':
        return None
    else: 
        df_filtered = df_filtered[df_filtered['variety'] == wine_type]
    max_points = max(df_filtered['points'])
    df_filtered = df[df['points'] == max_points]
    wine_name = df_filtered['title'].iloc[0]

    return str(wine_name.split(' (')[0])

@app.callback(
    Output('highest_value_name', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'))
def max_value_name(wine_type, state):
    if state == 'select your state':
        return None
    else:
        df_filtered = df[df['state'] == state]
    if wine_type == 'select a variety':
        return None
    else: 
        df_filtered = df_filtered[df_filtered['variety'] == wine_type]
    max_value = max(df_filtered['value'])
    df_filtered = df[df['value'] == max_value]
    wine_name = df_filtered['title'].iloc[0]
    return (wine_name.split(' (')[0] + '     ')

@app.callback(
    Output('highest_value', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'))
def max_value(wine_type, state):
    if state == 'select your state':
        return None
    else:
        df_filtered = df[df['state'] == state]
    if wine_type == 'select a variety':
        return None
    else: 
        df_filtered = df_filtered[df_filtered['variety'] == wine_type]
    max_value = max(df_filtered['value'])
    df_filtered = df[df['value'] == max_value]
    return str(str(round(max_value, 2)))

@app.callback(
    Output('wine_variety', 'options'),
    Input('province-widget', 'value'))
def wine_options(state):
    if state == 'select your state':
        df_filtered = df
    else:
        df_filtered = df[df['state'] == state]
    return [{'label': variety, 'value': variety} for variety in df_filtered['variety'].unique()]

@app.callback(
    Output('plots', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'),
    Input('wine_variety', 'value'))
def plot_altair(selected_province, price_value, points_value, wine_variety):
    if selected_province == 'select your state':
        df_filtered = df
    else:
        df_filtered = df[df['state'] == selected_province]
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    df_filtered = df_filtered.query("variety == @wine_variety")
    chart1 = alt.Chart(df_filtered).mark_point().encode(
        x=alt.X('price', scale=alt.Scale(zero=False)),
        y=alt.Y('points', scale=alt.Scale(zero=False)),
        color = 'variety',
        tooltip='title').interactive()
    
    chart2 = alt.Chart(df_filtered, title = 'Average Price of Selection').mark_bar().encode(
        y = alt.Y('mean(price)', title='Average Price ($)'),
        x = alt.X('variety', scale=alt.Scale(zero=False), axis=alt.Axis(labelAngle= -45),),
        color = 'variety',
        tooltip = alt.Tooltip('mean(price)', format='.2f')        
    )

    chart = chart1 | chart2
    return chart.to_html()

@app.callback(
    Output('maps', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'),
     Input('wine_variety', 'value'))
def plot_altair(selected_province, price_value, points_value,wine_variety):
    if selected_province == 'select your state':
        df_filtered = df
    else:
        df_filtered = df[df['state'] == selected_province]

    state_map = alt.topo_feature(data.us_10m.url, 'states')
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    df_filtered = df_filtered.query("variety == @wine_variety")
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

    colormap = alt.Scale(domain=[0, 100, 1000, 2000, 4000, 8000, 16000],
                         range=['#C7DBEA', '#CCCCFF', '#B8AED2', '#3A41C61',
                                '#9980D4', '#722CB7', '#663399'])

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
                stroke=None)
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)