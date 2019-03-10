# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from data.scrobbles import get_scrobbles
from data.artists import get_artists

from plots.plays_by_artist import get_artists_plays_at_work_plot
from plots.plays_by_artist import get_artists_plays_at_work_data
from plots.plays_by_artist import get_artists_plays_late_at_night
from plots.plays_by_artist import get_artists_plays_on_weekends
from plots.tags import top_tags_plot
from plots.artists import top_artists_plot

colors = ['#d7191c', '#2b83ba', '#abdda4', '#fdae61', '#ffff44']
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css','/static/custom.css']

print("Fetching scrobbles...")
scrobbles = get_scrobbles()

print("Fetching artists...")
artists = get_artists()

print("Fetching top tags...")
top_tags_trace, top_tags_layout = top_tags_plot(color=colors[0])

print("Fetching top artists...")
top_artists_trace, top_artists_layout = top_artists_plot(color=colors[1])

print("Fetching top artists at work...")
top_at_work = get_artists_plays_at_work_data(scrobbles, artists)

print("Fetching top late night artists...")
top_late_night = get_artists_plays_late_at_night(scrobbles, artists)

print("Fetching top weekend artists...")
top_weekends = get_artists_plays_on_weekends(scrobbles, artists)


work_div = html.Div(className='col-md-4', children=[
    html.Table(className='table table-borderless', children=[
        html.Tr(children=[
            html.Td(children=[
                html.H1("At Work")
            ]),
        ]),

        html.Tr(children=[
            html.Td(children=[
                html.H3("No scrobbles")
            ]),
        ])
    ])
])
print(len(top_at_work))
if len(top_at_work) > 0:
    work_div = html.Div(className='col-md-4', children=[
            html.Table(className='table table-borderless', children=[

                html.Tr(children=[
                    html.Td(children=[
                        html.H1("At Work")
                    ]),
                ]),

                html.Tr(children=[
                    html.Td(children=[
                        html.Img(className='gridbox', src=top_at_work.at[top_at_work.index[-1], 'ImageURL'])
                    ])
                ]),

                html.Tr(children=[
                    html.Td(children=[
                        html.H3(top_at_work.index[-1]),
                        html.H3('{} plays'.format(top_at_work.at[top_at_work.index[-1], 'PlayCount']))
                    ]),
                ])
            ]),
        ])

late_night_div = html.Div(className='col-md-4', children=[
    html.Table(className='table table-borderless', children=[
        html.Tr(children=[
            html.Td(children=[
                html.H1("Late At Night")
            ]),
        ]),

        html.Tr(children=[
            html.Td(children=[
                html.H3("No scrobbles")
            ]),
        ])
    ])
])
print(len(top_late_night))
if len(top_late_night) > 0:
    late_night_div = html.Div(className='col-md-4', children=[
        html.Table(className='table table-borderless', children=[

            html.Tr(children=[
                html.Td(children=[
                    html.H1("Late At Night")
                ]),
            ]),

            html.Tr(children=[
                html.Td(children=[
                    html.Img(className='gridbox', src=top_late_night.at[top_late_night.index[-1], 'ImageURL'])
                ])
            ]),

            html.Tr(children=[
                html.Td(children=[
                    html.H3(top_late_night.index[-1]),
                    html.H3('{} plays'.format(top_late_night.at[top_late_night.index[-1], 'PlayCount']))
                ]),
            ])
        ]),
    ])

weekends_div = html.Div(className='col-md-4', children=[
    html.Table(className='table table-borderless', children=[
        html.Tr(children=[
            html.Td(children=[
                html.H1("On Weekends")
            ]),
        ]),

        html.Tr(children=[
            html.Td(children=[
                html.H3("No scrobbles")
            ]),
        ])
    ])
])
print(len(top_weekends))
if len(top_weekends) > 0:
    weekends_div = html.Div(className='col-md-4', children=[
            html.Table(className='table table-borderless', children=[

                html.Tr(children=[
                    html.Td(children=[
                        html.H1("At Weekends")
                    ]),
                ]),

                html.Tr(children=[
                    html.Td(children=[
                        html.Img(className='gridbox', src=top_weekends.at[top_weekends.index[-1], 'ImageURL'])
                    ]),
                ]),

                html.Tr(children=[
                    html.Td(children=[
                        html.H3(top_weekends.index[-1]),
                        html.H3('{} plays'.format(top_weekends.at[top_weekends.index[-1], 'PlayCount']))
                    ]),
                ])
            ]),
        ])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className='container text-center', children=[
    # Title
    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            html.H1('Last Dash', className="display-1"),
        ])
    ]),

    # Tags and artists radial plots
    html.Div(className='row', children=[
        html.Div(className='col-md-6', children=[
            dcc.Graph(
                id='top_tags',
                figure={
                    'data': top_tags_trace,
                    'layout': top_tags_layout
                }
            )
        ]),
        html.Div(className='col-md-6', children=[
            dcc.Graph(
                id='top_artists',
                figure={
                    'data': top_artists_trace,
                    'layout': top_artists_layout
                }
            )
        ])
    ]),

    # Top artist at work, on weekends and late at night
    html.Div(className='row', children=[
        work_div,
        weekends_div,
        late_night_div,
        # html.Div(className='col-md-6', children=[
        #     dcc.Graph(
        #         id='top_at_work',
        #         figure={
        #             'data': plays_at_work_trace,
        #             'layout': plays_at_work_layout
        #         }
        #     )
        # ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)