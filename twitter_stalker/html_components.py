import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash_table import DataTable

from .constants import img_base64, twitter_lang_metadata_filename

twtr_lang_df = pd.read_csv(twitter_lang_metadata_filename)
twtr_lang_df = twtr_lang_df.sort_values('name')
lang_options = [{'label': loc_name, 'value': code}
                for loc_name, code in
                zip(twtr_lang_df['name'] + ' | ' + twtr_lang_df['local_name'],
                    twtr_lang_df['code'])]


Layout = html.Div([
    dcc.Loading(dcc.Store(id='twitter_df', storage_type='memory')),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H1('')
        ], lg=4, xs=15),
        dbc.Col([
            html.A([
                html.Img(src='data:image/png;base64,' + img_base64,
                         width=400, style={'display': 'inline-block'}),
            ]),
            html.Br(),
        ], lg=6, xs=15),
    ], style={'margin-left': '1%'}),
    html.Br(),
    dbc.Row([
        dbc.Col(lg=2, xs=10),
        dbc.Col([
           dcc.Dropdown(id='search_type',
                        options=[{'label': c, 'value': c}
                                 for c in ['Search Tweets',
                                           'Search Users',
                                           'Get User Timeline']],
                        value="Search Tweets",
                        style={'color':'black'}
                        )
        ], lg=2, xs=10),
        dbc.Col([
            dbc.Input(id='twitter_search',
                      placeholder='Search query'),
        ], lg=2, xs=10),
        dbc.Col([
            dbc.Input(id='twitter_search_count',
                      placeholder='Number of results', type='number',
                        style={'color':'black'}),

        ], lg=2, xs=10),
        dbc.Col([
            dcc.Dropdown(
                id='twitter_search_lang', placeholder='Language',
                         options=lang_options,
                         style={'position': 'relative', 'zIndex': 15, 'color':'black'},
                         ),
        ], lg=2, xs=10),
        dbc.Col([
            dbc.Button(id='search_button', children='Submit', outline=True, color='primary'),
        ], lg=2, xs=10),
    ]),
    html.Hr(),
    dbc.Container([
        dbc.Col(lg=2, xs=10),
        dbc.Tabs([
            dbc.Tab([
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Text field:',color='primary'),
                        dcc.Dropdown(id='text_columns',
                                     placeholder='Text Column',
                                     value='tweet_full_text'),
                    ], lg=3, xs=9,
                        style={'color':'black'}),
                    dbc.Col([
                        dbc.Label('Weighted by:',color='primary'),
                        dcc.Dropdown(id='numeric_columns',
                                     placeholder='Numeric Column',
                        style={'color':'black'},
                                     value='tweet_retweet_count'
                                     ),
                    ], lg=3, xs=9),
                    dbc.Col([
                        dbc.Label('Elements to count:',color='primary'),
                        dcc.Dropdown(id='regex_options',
                                     options=[{'label': x, 'value': x}
                                              for x in ['Words', 'Emoji',
                                                        'Mentions', 'Hashtags',
                                                        '2-word Phrases',
                                                        '3-word Phrases']],
                                     value='Words'),
                    ], lg=3, xs=9,
                        style={'color':'black'}),
                ]),
                html.Br(),
                html.H2(id='wtd_freq_chart_title',
                        style={'textAlign': 'center',
                        'color':'white',
                        'font':'white'}),
                dcc.Loading([
                    dcc.Graph(id='wtd_freq_chart',
                              config={'displayModeBar': False},
                              figure={'layout': go.Layout(plot_bgcolor='#878787',
                                                          paper_bgcolor='#878787')
                                      }),
                ]),
            ], label='Text Analysis', id='text_analysis_tab'),
            dbc.Tab([
                html.H3(id='user_overview', style={'textAlign': 'center','color':'white'}),
                dcc.Loading([
                    dcc.Graph(id='user_analysis_chart',
                              config={'displayModeBar': False},
                              figure={'layout': go.Layout(plot_bgcolor='#878787',
                                                          paper_bgcolor='#878787')
                                      })
                ]),
            ], tab_id='user_analysis_tab', label='User Analysis'),
        ], id='tabs'),
    ]),
    html.Hr(), html.Br(),
    dbc.Row([
        dbc.Col(lg=3, xs=11),
        dbc.Col(id='container_col_select',
                children=dcc.Dropdown(id='col_select',
                                      placeholder='Filter by:'),
                lg=2, xs=11,
                        style={'color':'black'}),
        dbc.Col([
            dbc.Col([
                dbc.Container(children=dcc.RangeSlider(id='num_filter',
                                                       updatemode='mouseup')),
                dbc.Container(children=html.Div(id='rng_slider_vals'),
                              style={'text-align': 'center'}),
            ], lg=0, xs=0, id='container_num_filter',
                style={'display': 'none'}),
            dbc.Col(id='container_str_filter',
                    style={'display': 'none'},
                    children=dcc.Input(id='str_filter'), lg=0, xs=0),
            dbc.Col(id='container_bool_filter',
                    style={'display': 'none'},
                    children=dcc.Dropdown(id='bool_filter',
                                          options=[{'label': 'True',
                                                    'value': 1},
                                                   {'label': 'False',
                                                    'value': 0}],
                        style={'color':'black'}),
                    lg=0, xs=0),
            dbc.Col(id='container_cat_filter',
                    style={'display': 'none'},
                    children=dcc.Dropdown(id='cat_filter', multi=True,
                        style={'color':'black'}),
                    lg=0, xs=0),
            dbc.Col([
                dcc.DatePickerRange(id='date_filter'),
            ], id='container_date_filter', style={'display': 'none','color':'white'},
                lg=0, xs=0),
        ], style={'width': '20%', 'display': 'inline-block'}),
        dbc.Col(id='row_summary', lg=2, xs=11),
        dbc.Col(html.A('Download Table', id='download_link',
                       download="rawdata.csv", href="", target="_blank",
                       n_clicks=0), lg=2, xs=11),
    ], style={'position': 'relative', 'zIndex': 5}),
    dbc.Row([
        dbc.Col([
            dbc.Label('Add/remove columns: ',color='primary'),
            dcc.Dropdown(id='output_table_col_select', multi=True,
                         value=['tweet_created_at', 'user_screen_name',
                                'user_followers_count', 'tweet_full_text',
                                'user_location']
                         ),
        ], lg=2, xs=11, style={'margin-left': '1%','color':'black'}),
        dbc.Col([
            html.Br(),
            dcc.Loading(
                DataTable(id='table', sort_action='native',
                          virtualization=True,
                          fixed_rows={'headers': True},
                          style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                          style_cell_conditional=[{
                              'if':{'column_id':'tweet_full_text'},
                              'textAlign':'left'
                          }],
                          style_cell={'width': '200px',
                                      'font-family': 'Source Sans Pro',
                                      'textAlign':'center',
                                      'color':'white',
                                      'backgroundColor':'rgb(50, 50, 50)'}),
            ),
        ], lg=9, xs=11, style={'position': 'relative', 'zIndex': 1,
                               'margin-left': '1%'}),
    ] + [html.Br() for x in range(30)]),
])
