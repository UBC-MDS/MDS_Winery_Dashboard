import dash
import dash_html_components as html
import dash_core_components as dcc
import altair as alt
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from vega_datasets import data

alt.data_transformers.disable_max_rows()

# # Path
# BASE_PATH = pathlib.Path(__file__).parent.parent.resolve()
# DATA_PATH = BASE_PATH.joinpath('data').resolve()

# #Read data
# df = pd.read_csv(DATA_PATH.joinpath('processed', 'cleaned_data.csv'))

df = pd.read_csv('data/processed/cleaned_data.csv') #data/processed/cleaned_data.csv
df = df.query('country == "US"') 
df['title'] = df['title'].str.split('(',expand=True)
display_df = df[['title', 'variety', 'state', 'points', 'price']]
display_df = display_df.rename(columns={'title': 'Title', 'variety':'Variety', 'state':'State', 'points':'Points', 'price':'Price'})
app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

colors = {
    'background': '#111111',
    'text': '#522889'
}

collapse = html.Div(
    [
        dbc.Button(
            "Learn more",
            id="collapse-button",
            className="mb-3",
            outline=False,
            style={'margin-top': '10px',
                'width': '150px',
                'background-color': 'white',
                'color': 'steelblue'}
        ),
    ]
)

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# header = html.Div(children=[
#     html.Div(
#         children=html.Img(
#             src="C:/Users/mgaro/UBC-MDS/DSCI_532/MDS_Winery_Dashboard/src/black.jpg",
#             style={
#                 'maxWidth': '100%',
#                 'maxHeight': '100%',
#                 'marginLeft': 'auto',
#                 'marginRight': 'auto'
#             }
#         ),
#         style={
#             'width': 400,
#             'height': 200,
#             'border': 'thin grey solid'
#         }
#     )
# ])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('MDS WINERY DASHBOARD', className="app__header__title"),
            # dbc.Collapse(html.P(
            #     """
            #     Let me introduce our MDS winery dashboard to you =)
            #     """,
            #     className="app__header__title--grey",
            # ), 
            # id='collapse'),
        ], 
        md=12),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Col([collapse,
                dbc.Collapse(html.P(
                """
                Let me introduce our MDS winery dashboard to you =)
                """,
                className="app__header__title--grey",
            ), 
            id='collapse')])
    ], style={'backgroundColor': '#BD93D3', 'border-radius': 5, 'padding': 15, 'margin-top': 22, 'margin-bottom': 22, 'margin-right': 11}),
#    html.H1('MDS Winery Dashboard', style={
#          'textAlign': 'center',
#          'color': '#522889', 'font-size': '27px', 'text-decoration': 'underline'

#       }), 

    dcc.Tabs([
        dcc.Tab([
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
                        'State Selection'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }),
                    dcc.Dropdown(
                        id='province-widget',
                        value='select your state',  
                        options=[{'label': state, 'value': state} for state in df['state'].unique()],
                        multi=True,
                        placeholder='Select a State'
                    ),
                    html.Br(),
                    html.Label(['Wine Type'], style={'color': '#7a4eb5', "font-weight": "bold"}
                    ),
                    dcc.Dropdown(
                        id='wine_variety',
                        value='select a variety', 
                        placeholder='Select a Variety', 
                        multi=True
                    ),
                    html.Br(),
                    html.Label(['Price Range'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='price',
                        min=df['price'].min(),
                        max=df['price'].max(),
                        value=[df['price'].min(), df['price'].max()],
                        marks = {4: '$4', 25: '$25', 50: '$50', 75: '$75', 100: '$100','color': '#7a4eb5'}
                    ),
                    html.Label(['Points Range'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='points',
                        min=df['points'].min(),
                        max=df['points'].max(),
                        value=[df['points'].min(), df['points'].max()],
                        marks = {80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}
                        ),
                    html.Label(['Value Ratio'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(min=0, 
                        max=1, 
                        step=0.1, 
                        value=[0.2,0.6], 
                        marks = {0: '0', 0.2: '0.2', 0.4: '0.4', 0.6: '0.6', 0.8: '0.8', 1: '1'}  
                    ),
                    html.Br(),

                    html.Button(id="reset-btn", children="RESET", n_clicks=0)
                    
                    ], md=4,
                ),
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
                        html.H5(['Highest Value Wine:']),
                        html.Br(),
                        html.H5(
                            id = 'highest_value_name'),
                        html.Br(),
                        html.H4(
                            id = 'highest_value'),
                        ], style={'border': '1px solid #d3d3d3', 'padding-left': '10%','padding-top': '2%', 'padding-right': '10%', 'height': '180px', 'border': '1px solid', 'backgroundColor' : '#3c1a69', 
                        'color': '#ffff', 'font-size': '7px'}),  
                    html.Br(),     
                    dbc.Row([
                        dbc.Col([
                            html.H5(['Highest Wine Score:']),
                            html.Br(),
                            html.H5(
                                id='highest_score_name'),
                            html.Br(),
                            html.H4(
                                id='highest_score'),
                        ], style={'border': '1px solid #d3d3d3', 'padding-left': '10%', 'padding-top': '2%','padding-right': '10%', 'height': '180px', 'border': '1px solid', 'backgroundColor' : '#3c1a69', 
                        'color': '#ffff', 'font-size': '7px'}),
                        ])
                    ])
                ]),
            ], label='MDS Winery'),
        dcc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Label([
                        'State Selection'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }),
                    dcc.Dropdown(
                        id='table_state',
                        value='Oregon',  
                        options=[{'label': state, 'value': state} for state in df['state'].unique()],
                        multi=True,
                        placeholder='Select a State'
                    ),
                    html.Br(),
                    html.Label(['Wine Type'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.Dropdown(
                        id='table_variety',
                        value='Red Wine', 
                        placeholder='Select a Variety', 
                        multi=True
                    ),
                    html.Br(),
                    html.Label(['Price Range'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='table_price',
                        min=df['price'].min(),
                        max=df['price'].max(),
                        value=[df['price'].min(), df['price'].max()],
                        marks = {4: '$4', 25: '$25', 50: '$50', 75: '$75', 100: '$100','color': '#7a4eb5'}
                    ),
                    html.Label(['Points Range'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='table_points',
                        min=df['points'].min(),
                        max=df['points'].max(),
                        value=[df['points'].min(), df['points'].max()],
                        marks = {80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}
                        ),
                    html.Label(['Value Ratio'], style={
                'color': '#7a4eb5', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(min=0, 
                        max=1, 
                        step=0.1, 
                        value=[0.2,0.6], 
                        marks = {0: '0', 0.2: '0.2', 0.4: '0.4', 0.6: '0.6', 0.8: '0.8', 1: '1'}  
                    ),
                ], md=4,),
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": col, "id": col} for col in display_df.columns[:]], 
                        data=display_df.to_dict('records'),
                        page_size=11,
                        sort_action='native',
                        style_header = {'textAlign': 'left'},
                        style_data = {'textAlign': 'left'},
                    ),
                ], md=8)
            ]),
            dbc.Row([
                html.Iframe(
                        id = 'table_plots',
                        style={'border-width': '0', 'width': '100%', 'height': '500px'})
                ])     
        ],label='Data')]),
])



    

@app.callback(
    Output('highest_score', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'))
def max_score(wine_type, state):
    if state == 'select your state':
        return None
    else:
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
        else:
            df_filtered = df[df['state'] == state]
    if wine_type == 'select a variety' or wine_type is None:
        return None
    else: 
        if type(wine_type) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_type)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_type")  
    max_points = max(df_filtered['points'])
    df_filtered = df[df['points'] == max_points]
    wine_name = df_filtered['title'].iloc[0]

    return str(str(round(max_points,2)))


@app.callback(
    Output('highest_score_name', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'))
def max_score_name(wine_type, state):
    if state == 'select your state':
        return None
    else:
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
        else:
            df_filtered = df[df['state'] == state]
    if wine_type == 'select a variety' or wine_type is None:
        return None
    else: 
        if type(wine_type) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_type)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_type") 
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
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
        else:
            df_filtered = df[df['state'] == state]
    if wine_type == 'select a variety' or wine_type is None:
        return None
    else: 
        if type(wine_type) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_type)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_type")  
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
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
        else:
            df_filtered = df[df['state'] == state]
    if wine_type == 'select a variety' or wine_type is None:
        return None
    else: 
        if type(wine_type) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_type)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_type") 
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
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
        else:
            df_filtered = df[df['state'] == state]
    return [{'label': variety, 'value': variety} for variety in df_filtered['variety'].unique()]

@app.callback(
    Output('table_variety', 'options'),
    Input('table_state', 'value'))
def wine_options(state):
    if state == 'select your state':
        df_filtered = df
    else:
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
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
        if type(selected_province) == list:
            df_filtered = df[df['state'].isin(selected_province)]
        else:
            df_filtered = df[df['state'] == selected_province]
    if type(wine_variety) == list:
        df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
    else:  
        df_filtered = df_filtered.query("variety == @wine_variety")   

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    
    selection = alt.selection_single(    
        fields=['variety'], # limit selection to the Major_Genre field
        bind='legend')

    chart1 = alt.Chart(df_filtered).mark_point().encode(
        x=alt.X('price', scale=alt.Scale(zero=False)),
        y=alt.Y('points', scale=alt.Scale(zero=False)),
        color = alt.Color('variety'),
        opacity = alt.condition(selection, alt.value(0.7), alt.value(0.3)), # scale=alt.Scale(scheme='bluepurple')),
        tooltip='title').add_selection(selection).interactive()
    
    chart2 = alt.Chart(df_filtered, title = 'Average Price of Selection').mark_bar().encode(
        y = alt.Y('mean(price)', title='Average Price ($)'),
        x = alt.X('variety', scale=alt.Scale(zero=False), axis=alt.Axis(labelAngle= -45),),
        color = 'variety',
    )

    chart = chart1 | chart2
    return chart.to_html()

@app.callback(
    Output('maps', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'),
    Input('wine_variety', 'value'))
def plot_map(state, price_value, points_value,wine_variety):
    if state == 'select your state':
        df_filtered = df
    else:
        if type(state) == list:
            df_filtered = df[df['state'].isin(state)]
        else:
            df_filtered = df[df['state'] == state]

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
        fill='#EAEDED',
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

@app.callback(
    Output('table', 'data'),
    Input('table_state', 'value'),
    Input('table_price', 'value'),
    Input('table_points', 'value'),
    Input('table_variety', 'value'))
def table(state, price, points, variety):
    if state == 'select your state':
        df_filtered = display_df
    else:
        if type(state) == list:
            df_filtered = display_df[display_df['State'].isin(state)]
        else:
            df_filtered = display_df[display_df['State'] == state]
    if type(variety) == list:
        df_filtered = df_filtered[df_filtered['Variety'].isin(variety)]
    else:  
        df_filtered = df_filtered.query("Variety == @variety")   

    df_filtered = df_filtered[(df_filtered['Price'] >= min(price)) & (df_filtered['Price'] <= max(price))]
    df_filtered = df_filtered[(df_filtered['Points'] >= min(points)) & (df_filtered['Points'] <= max(points))]
   
    return df_filtered.to_dict('records')

# @app.callback(
#     Output('table_plots', 'srcDoc'),
#     Input('table_state', 'value'),
#     Input('table_price', 'value'),
#     Input('table_points', 'value'),
#     Input('table_variety', 'value'))
# def table_plot(selected_province, price_value, points_value, wine_variety):
#     if selected_province == 'select your state':
#         df_filtered = df
#     else:
#         if type(selected_province) == list:
#             df_filtered = df[df['state'].isin(selected_province)]
#         else:
#             df_filtered = df[df['state'] == selected_province]
#     if type(wine_variety) == list:
#         df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
#     else:  
#         df_filtered = df_filtered.query("variety == @wine_variety")   

#     df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
#     df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    
#     selection = alt.selection_single(    
#             fields=['variety'], # limit selection to the Major_Genre field
#             bind='legend')

#     chart = alt.Chart(df_filtered).mark_point().encode(
#         x=alt.X('price', scale=alt.Scale(zero=False)),
#         y=alt.Y('points', scale=alt.Scale(zero=False)),
#         color = alt.Color('variety'),#, scale=alt.Scale(scheme='bluepurple')),
#         opacity = alt.condition(selection, alt.value(1), alt.value(0.025)),
#         tooltip='title').add_selection(selection).interactive()
    
#     return chart.to_html()

@app.callback(
    Output('table_plots', 'srcDoc'),
    Input('table_state', 'value'),
    Input('table_price', 'value'),
    Input('table_points', 'value'),
    Input('table_variety', 'value'))
def table_plot(selected_province, price_value, points_value, wine_variety):
    if selected_province == 'select your state':
        df_filtered = df
    else:
        if type(selected_province) == list:
            df_filtered = df[df['state'].isin(selected_province)]
        else:
            df_filtered = df[df['state'] == selected_province]
    if type(wine_variety) == list:
        df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
    else:  
        df_filtered = df_filtered.query("variety == @wine_variety")   

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    
    selection = alt.selection_multi(    
            fields=['variety'], # limit selection to the Major_Genre field
            bind='legend')

    select_price = alt.selection_interval(empty='all', encodings=['x'])
    select_points= alt.selection_interval(empty='all', encodings=['x'])

    multidim_legend = alt.Chart(df_filtered).mark_point(filled=True).encode(
        x=alt.X('state'),
        y=alt.Y('variety', axis=None),
        size =alt.Size('count()', legend=None),
        color = alt.Color('variety'),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(selection).properties(height=100, width=100)

    price_slider = alt.Chart(df_filtered).mark_bar().encode(
    alt.X('price', title='', axis=alt.Axis(grid=False),
          scale=alt.Scale(domain=[0, 110])),
    alt.Y('count()', title='', axis=None)
    ).properties(height=40, width=100).add_selection(select_price)

    points_slider = alt.Chart(df_filtered).mark_bar().encode(
    alt.X('points', title='', axis=alt.Axis(grid=False),
          scale=alt.Scale(domain=[75, 105])),
    alt.Y('count()', title='', axis=None)
    ).properties(height=40, width=100).add_selection(select_points)

    # text = alt.Chart(df_filtered).mark_text().encode(
    #     y=alt.y('title',axis=None))

    chart1 = alt.Chart(df_filtered).mark_point().encode(
        x=alt.X('price', scale=alt.Scale(zero=False)),
        y=alt.Y('points', scale=alt.Scale(zero=False)),
        color = alt.Color('variety'),#, scale=alt.Scale(scheme='bluepurple')),
        opacity = alt.condition(select_price & select_points & selection, alt.value(0.5), alt.value(0)),
        tooltip='title').add_selection(selection).interactive()
    
    chart = chart1|(price_slider & points_slider & multidim_legend)
    return chart.to_html()





@app.callback(
    Output('table_state', 'value'),
    Output('table_variety', 'value'),
    Output('table_points', 'value'),
    Output('table_price', 'value'),
    Input('province-widget', 'value'),
    Input('wine_variety', 'value'),
    Input('points', 'value'),
    Input('price', 'value'))
def cross_tab_update_price(state, variety, points, price):
    return state, variety, points, price


# reset callback
@app.callback(
    Output('province-widget', 'value'),
    [Input('reset-btn', 'n_clicks')],
)
def resetAll(n_clicks):
    if n_clicks > 0:
        return (['select your state'])


if __name__ == '__main__':
    app.run_server(debug=True)