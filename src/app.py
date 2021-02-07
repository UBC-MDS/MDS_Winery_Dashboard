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

########## Additional Data Filtering ###########################################
df = pd.read_csv('data/processed/cleaned_data.csv') #data/processed/cleaned_data.csv
df = df.query('country == "US"') 
df = df.dropna(subset=['price', 'points', 'title'])
df[['price']] = df[['price']].astype(int)
df['title'] = df['title'].str.split('(',expand=True)
stats = df.groupby('variety').count()
filter = list(stats.sort_values('title', ascending=False)[0:10].reset_index().loc[:,'variety'])
df = df[df['variety'].isin(filter)].dropna(subset=['price', 'points', 'title'])
display_df = df[['title', 'variety', 'state', 'points', 'price']]
display_df = display_df.rename(columns={'title': 'Title', 'variety':'Variety', 'state':'State', 'points':'Points', 'price':'Price'})
###############################################################################


app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
# Set the app title
app.title = "MDS Winery"
server=app.server

colors = {
    'background': "#111111",
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
                'color': '#522889'}
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


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('MDS Winery Dashboard', style={'text-align': 'center', 'color': 'white', 'font-size': '40px', 'font-family': 'Georgia'}),
            dbc.Collapse(html.P(
                """
                The dashboard will help you with your wine shopping today. Whether you desire crisp Californian Chardonnay or bold Cabernet Sauvignon from Texas, simply select a state and the wine type. The results will help you to choose the best wine for you.
                """,
                style={'color': 'white', 'width': '70%'}
            ), id='collapse'),
        ], md=10),
        dbc.Col([collapse])
    ], style={'backgroundColor': '#522889', 'border-radius': 3, 'padding': 15, 'margin-top': 22, 'margin-bottom': 22, 'margin-right': 11}),

    dcc.Tabs([
        dcc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Label([
                        'State Selection'], style={
                'color': '#522889', "font-weight": "bold"
            }),
                    dcc.Dropdown(
                        id='province-widget',
                        value='select your state',  
                        options=[{'label': state, 'value': state} for state in df['state'].sort_values().unique()],
                        multi=True,
                        placeholder='Select a State'
                    ),
                    html.Br(),
                    html.Label(['Wine Type'], style={'color': '#522889', "font-weight": "bold"}
                    ),
                    dcc.Dropdown(
                        id='wine_variety',
                        value='select a variety', 
                        placeholder='Select a Variety', 
                        multi=True
                    ),
                    html.Br(),
                    html.Label(['Price Range'], style={
                'color': '#522889', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='price',
                        min=df['price'].min(),
                        max=df['price'].max(),
                        value=[df['price'].min(), df['price'].max()],
                        marks = {4: '$4', 25: '$25', 50: '$50', 75: '$75', 100: '$100','color': '#522889'}
                    ),
                    html.Label(['Points Range'], style={
                'color': '#522889', "font-weight": "bold"
            }
                    ),
                    dcc.RangeSlider(
                        id='points',
                        min=df['points'].min(),
                        max=df['points'].max(),
                        value=[df['points'].min(), df['points'].max()],
                        marks = {80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}
                        ),
                    html.Br(),
                    dbc.Button('Reset', id = 'reset-btn-1', n_clicks=0, className='reset-btn-1'),                  
                    ], style={'border': '1px solid', 'border-radius': 3, 'padding': 15, 'margin-top': 22, 'margin-bottom': 22, 'margin-right': 0}, md=4,
                ),
                dbc.Col([
                    html.Iframe(
                        id = 'maps',
                        style={'border-width': '0', 'width': '100%', 'height': '460px'})
                    ], md=8)
                ]),
            dbc.Row([
                    dbc.Col([
                    html.Br(),
                    dbc.Row([
                            dbc.Card([
                                dbc.CardHeader('Highest Value Wine:', 
                                style={'fontWeight': 'bold', 'color':'white','font-size': '22px', 'backgroundColor':'#522889','width': '100%', 'height': '50px'}),
                                dbc.CardBody(id='highest_value_name', style={'color': '#522889', 'fontSize': 18, 'width': '300px', 'height': '70px'}),
                            dbc.CardBody(
                                id='highest_value', style={'color': '#522889', 'fontSize': 18, 'width': '300px', 'height': '70px'})])]),
                    html.Br(),     
                    dbc.Row([
                            dbc.Card([
                                dbc.CardHeader('Highest Score Wine:', 
                                style={'fontWeight': 'bold', 'color':'white','font-size': '22px', 'backgroundColor':'#522889', 'width': '100%', 'height': '50px'}),
                                dbc.CardBody(id='highest_score_name', style={'color': '#522889', 'fontSize': 18, 'width': '300px', 'height': '70px'}),
                            dbc.CardBody(
                                id='highest_score',style={'color': '#522889', 'fontSize': 18, 'width': '300px', 'height': '70px'}),
                        ]),
                        ])
                    ], md = 3),
                dbc.Col([
                    
                    html.Iframe(
                        id = 'plots',
                        style={'border-width': '0', 'width': '100%', 'height': '510px'})
                    ]),

                ]),
            ], label='MDS Winery'),
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
                'color': '#522889', "font-weight": "bold"
            }),
                    dcc.Dropdown(
                        id='table_state',
                        value='select your state',  
                        options=[{'label': state, 'value': state} for state in df['state'].sort_values().unique()],
                        multi=True,
                        placeholder='Select a State'
                    ),
                    html.Br(),
                    html.Label(['Wine Type'], style={
                'color': '#522889', "font-weight": "bold"
            }
                    ),
                    dcc.Dropdown(
                        id='table_variety',
                        value='select a variety', 
                        placeholder='Select a Variety', 
                        multi=True
                    ),
                    html.Br(),
                    html.Label(['Price Range'], style={
                'color': '#522889', "font-weight": "bold"
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
                'color': '#522889', "font-weight": "bold"
            }
                    ),
                    
                    dcc.RangeSlider(
                        id='table_points',
                        min=df['points'].min(),
                        max=df['points'].max(),
                        value=[df['points'].min(), df['points'].max()],
                        marks = {80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}, className='slider'
                        ),
                    html.Br(),
                    dbc.Button('Reset', id = 'reset-btn-2', n_clicks=0, className='reset-btn-2'),
                ],style={'border': '1px solid', 'border-radius': 3, 'padding': 15, 'margin-top': 22, 'margin-bottom': 22, 'margin-right': 0}, md=4),
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": col, "id": col} for col in display_df.columns[:]], 
                        data=display_df.to_dict('records'),
                        page_size=10,
                        sort_action='native',
                        filter_action='native',
                        style_header = {'textAlign': 'left'},
                        style_data = {'textAlign': 'left'},
                        style_cell_conditional=[
                            {'if': {'column_id': 'Title'},
                            'width': '50%'},
                            {'if': {'column_id': 'Price'},
                            'width': '9%'},
                            {'if': {'column_id': 'Points'},
                            'width': '10%'}],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0
                        },
                        # style_cell={
                        #     'whiteSpace': 'normal',
                        #     'height': 'auto',
                        # },
                    ),
                ], md=8)
            ]),
            dbc.Row([
                
                dbc.Col([
                    html.Br(),
                    html.Iframe(
                        id = 'table_plots',
                        style={'border-width': '0', 'width': '100%', 'height': '600px'})]),
                dbc.Col([
                dcc.Dropdown(
                        id='axis',
                        value='price',  
                        options=[{'label': "price", 'value': "price"}, 
                        {'label': "points", 'value': "points"}]
                ),
                html.Iframe(
                        id = 'heat_plot',
                        style={'border-width': '0', 'width': '100%', 'height': '100%'})])
                ])     
        ],label='Data')]),
])
    

@app.callback(
    Output('highest_score', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def max_score(wine_variety, selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    if wine_variety == 'select a variety':
         df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    if len(df_filtered):
        max_score = max(df_filtered['points'])
        df_filtered = df_filtered[df_filtered['points'] == max_score]
        max_score = str(round(max_score, 2))
    else:
        max_score = None
    
    
    return max_score


@app.callback(
    Output('highest_score_name', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def max_score_name(wine_variety, selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    if wine_variety == 'select a variety':
         df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    
    if len(df_filtered):
        max_points = max(df_filtered['points'])
        df_filtered = df_filtered[df_filtered['points'] == max_points]
        wine_name = df_filtered['title'].iloc[0]
        wine_name = str(wine_name.split(' (')[0])
    else:
        wine_name = 'No Wines Available'

    return wine_name

@app.callback(
    Output('highest_value_name', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def max_value_name(wine_variety, selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    if wine_variety == 'select a variety':
         df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    
    if len(df_filtered):
        max_value = max(df_filtered['value'])
        df_filtered = df_filtered[df_filtered['value'] == max_value]
        wine_name = df_filtered['title'].iloc[0]
        wine_name = wine_name.split(' (')[0] + '     '
    else: 
        wine_name = 'No Wines Available'
    return wine_name

@app.callback(
    Output('highest_value', 'children'),
    Input('wine_variety', 'value'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def max_value(wine_variety, selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    if wine_variety == 'select a variety':
         df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]

    if len(df_filtered):
        max_value = max(df_filtered['value'])
        df_filtered = df_filtered[df_filtered['value'] == max_value]
        max_value = str(round(max_value, 2))
    else:
        max_value = None
    
    
    return max_value
  
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
    return [{'label': variety, 'value': variety} for variety in df_filtered['variety'].sort_values().unique()]

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
    return [{'label': variety, 'value': variety} for variety in df_filtered['variety'].sort_values().unique()]


@app.callback(
    Output('plots', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'))
def plot_altair(selected_state, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    # filterng data based on wine variety selection
    # if wine_variety == 'select a variety':
    #     df_filtered = df_filtered
    # else:
    #     if type(wine_variety) == list:
    #         df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
    #     else:  
    #         df_filtered = df_filtered.query("variety == @wine_variety")

    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]

    data = df_filtered.groupby('variety')[['price', 'points']].mean()


    new_data = data.sort_values(by='price', ascending=False).head(10).reset_index()

    click = alt.selection_multi(fields=['variety'])
    
    ranked_bar1= (alt.Chart(new_data).mark_bar().encode(
        alt.X('variety' +':N', 
        sort=alt.EncodingSortField(
            field='points',  
            op="sum",  
            order='descending'
            )),
        alt.Y('points' + ':Q', title='Rating',
        scale=alt.Scale(domain=[min(new_data['points']),
        max(new_data['points'])])),
        color=alt.Color('variety',scale=alt.Scale(scheme='bluepurple'), legend=None),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)))

.add_selection(click)).properties(title="Wine Variety Average Ratings", width=300, height=300).interactive()

    
    ranked_bar = (alt.Chart(new_data).mark_bar().encode(
        alt.X('variety' +':N', 
        sort=alt.EncodingSortField(
            field='price',  
            op="sum",  
            order='descending'
            )),
        alt.Y('price' + ':Q', title='Price($)',
        scale=alt.Scale(domain=[min(new_data['price']),
        max(new_data['price'])])),
        color=alt.Color('variety',scale=alt.Scale(scheme='bluepurple'), legend=None),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)))
.add_selection(click)).properties(title="Wine Variety Average Prices", width=300, height=300).interactive()
    chart = (ranked_bar1 | ranked_bar).configure_axisX(
                labelAngle=60).configure_axis(
                                labelFontSize=12,
                                titleFontSize=12).configure_title(fontSize=16,
                                anchor='middle')
    return chart.to_html()

@app.callback(
    Output('maps', 'srcDoc'),
    Input('province-widget', 'value'),
    Input('price', 'value'),
    Input('points', 'value'),
    Input('wine_variety', 'value'))
def plot_map(selected_state, price_value, points_value,wine_variety):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    # filterng data based on wine variety selection
    if wine_variety == 'select a variety':
        df_filtered = df_filtered
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")

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


    map_click = alt.selection_multi(fields=['State'])
    states = alt.topo_feature(data.us_10m.url, "states")

    
    colormap = alt.Scale(domain=[0, 100, 1000, 2000, 4000, 8000, 16000, 32000],
                         range=['#C7DBEA', '#CCCCFF', '#B8AED2', '#3A41C61',
                                '#9980D4', '#722CB7', '#663399', '#512888'])


    foreground = (alt.Chart(states).mark_geoshape().encode(
        color=alt.Color('Num Reviews:Q', scale=colormap), opacity=alt.condition(map_click, alt.value(1), alt.value(0.2)),

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
    ).add_selection(map_click)
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

    if variety == "select a variety":
        df_filtered = df_filtered
    else:
        if type(variety) == list:
            df_filtered = df_filtered[df_filtered['Variety'].isin(variety)]
        else:  
            df_filtered = df_filtered.query("Variety == @variety")   

    df_filtered = df_filtered[(df_filtered['Price'] >= min(price)) & (df_filtered['Price'] <= max(price))]
    df_filtered = df_filtered[(df_filtered['Points'] >= min(points)) & (df_filtered['Points'] <= max(points))]

    df_filtered = df_filtered.astype(str)
    return df_filtered.to_dict('records')

@app.callback(
    Output('table_plots', 'srcDoc'),
    Input('table_state', 'value'),
    Input('table_price', 'value'),
    Input('table_points', 'value'),
    Input('table_variety', 'value'))
def table_plot(selected_state, price_value, points_value, wine_variety):
    if selected_state == 'select your state':
        df_filtered = df[df['state']=="New York"]
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    # filterng data based on wine variety selection
    if wine_variety == 'select a variety':
        df_filtered = df_filtered[df_filtered['variety']=="Red Blend"]
    else:
        if type(wine_variety) == list:
            df_filtered = df_filtered[df_filtered['variety'].isin(wine_variety)]
        else:  
            df_filtered = df_filtered.query("variety == @wine_variety")
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]
    
    selection = alt.selection_multi(    
            fields=['variety']) # limit selection to the Major_Genre field)

    select_price = alt.selection_interval(empty='all', encodings=['x'])
    select_points= alt.selection_interval(empty='all', encodings=['x'])

    multidim_legend = alt.Chart(df_filtered).mark_point(filled=True).encode(
        x=alt.X('variety', axis=None),
        y=alt.Y('state', title=''),
        size =alt.Size('count()', legend=None),
        color = alt.Color('variety'),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(selection).properties(height=40, width=110)

    price_slider = alt.Chart(df_filtered).mark_bar().encode(
    alt.X('price', title='Price $', axis=alt.Axis(grid=False),
          scale=alt.Scale(domain=[0, 110])),
    alt.Y('count()', title='', axis=None)
    ).properties(height=40, width=110).add_selection(select_price)

    points_slider = alt.Chart(df_filtered).mark_bar().encode(
    alt.X('points', title='Points', axis=alt.Axis(grid=False),
          scale=alt.Scale(domain=[75, 105])),
    alt.Y('count()', title='', axis=None)
    ).properties(height=40, width=110).add_selection(select_points)

    # text = alt.Chart(df_filtered).mark_text().encode(
    #     y=alt.y('title',axis=None))

    chart1 = alt.Chart(df_filtered).mark_point().encode(
        x=alt.X('price', scale=alt.Scale(zero=False), title = "Price($)"),
        y=alt.Y('points', scale=alt.Scale(zero=False), title = "Rating"),
        color = alt.Color('variety', legend=alt.Legend(columns=4)),#, scale=alt.Scale(scheme='bluepurple')),
        opacity = alt.condition(select_price & select_points & selection, alt.value(0.7), alt.value(0)),
        tooltip='title').add_selection(selection).interactive()
    
    chart = (chart1 & (multidim_legend | price_slider | points_slider )).configure_legend(orient='bottom').properties(
                            title="Rating vs Price"
                            ).configure_axis(
                                labelFontSize=14,
                                titleFontSize=14). configure_title(fontSize=16,
                                anchor='middle')

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

@app.callback(
    Output('heat_plot', 'srcDoc'),
    Input('table_state', 'value'),
    Input('axis', 'value'),
    Input('table_price', 'value'),
    Input('table_points', 'value'))
def plot_heat(selected_state,axis, price_value, points_value):
    if selected_state == 'select your state':
        df_filtered = df
    else:
        if type(selected_state) == list:
            df_filtered = df[df['state'].isin(selected_state)]
        else:
            df_filtered = df[df['state'] == selected_state]
    df_filtered = df_filtered[(df_filtered['price'] >= min(price_value)) & (df_filtered['price'] <= max(price_value))]
    df_filtered = df_filtered[(df_filtered['points'] >= min(points_value)) & (df_filtered['points'] <= max(points_value))]

    if axis == 'price':
        heatmap = alt.Chart(df_filtered.query('price < 100')).mark_rect().encode(
            x=alt.X("price" + ':Q',
            bin=alt.Bin(maxbins=10),
            title= "Price($)"),
            y=alt.Y('variety:O', 
                    title="Wine Variety"),
                    color=alt.Color('average(points):Q',
                    scale=alt.Scale(scheme="bluepurple"),
                    legend=alt.Legend(
                        orient='bottom', title="Average rating")
                        ),
                        tooltip=[alt.Tooltip('average(points):Q', format='.2f'),
                        alt.Tooltip('average(price)', format='$.2f'),
                        alt.Tooltip('average(value)', format='.2f'),
                        alt.Tooltip('count(title)')]
                        ).properties(
                            title="Average price for Popular Varieties"
                            ).configure_axis(
                                labelFontSize=12,
                                titleFontSize=12,
                                grid=False,
                                labelAngle=0). properties(width=300, height=300)
    if axis == "points":
        heatmap = alt.Chart(df_filtered).mark_rect().encode(
            x=alt.X("points" + ':Q',
            bin=alt.Bin(maxbins=10),
            title= "Rating Score"),
            y=alt.Y('variety:O', 
                    title="Wine Variety"),
                    color=alt.Color('average(price):Q',
                    scale=alt.Scale(scheme="bluepurple"),
                    legend=alt.Legend(
                        orient='bottom', title="Average price")
                        ),
                        tooltip=[alt.Tooltip('average(points):Q', format='.2f'),
                        alt.Tooltip('average(price)', format='$.2f'),
                        alt.Tooltip('average(value)', format='.2f'),
                        alt.Tooltip('count(title)')]
                        ).properties(
                            title="Average rating for Popular Varieties"
                            ).configure_axis(
                                labelFontSize=12,
                                titleFontSize=12,
                                grid=False,
                                labelAngle=0). properties(width=300, height=300)
    return heatmap.to_html()

# reset-btn-1
@app.callback(
    Output('province-widget', 'value'),
    Output('wine_variety', 'value'),
    Output('price', 'value'),
    Output('points', 'value'),
    [Input('reset-btn-1', 'n_clicks')])

def reset_1(clicks):
    if clicks==0:
        return
    else:
        res1 = 'select your state'
        res2 = 'select a variety'
        res3 = [df.price.min(), df.price.max()]
        res4 = [df.points.min(), df.points.max()]
        return res1, res2, res3, res4

# reset-btn-2
@app.callback(
    Output('reset-btn-1', 'n_clicks'),
    [Input('reset-btn-2', 'n_clicks')])

def reset_2(clicks):
    if clicks == 0:
        return 
    else:
        return clicks


if __name__ == '__main__':
    app.run_server(debug=True)