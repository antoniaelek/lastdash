# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from data.scrobbles import get_scrobbles
from data.scrobbles import get_obsessions
from data.scrobbles import get_loved_tracks
from plots.tags import top_tags_plot
from plots.artists import top_artists_plot
from plots.scrobbles import activity_plot

colors = ['#d7191c', '#2b83ba', '#abdda4', '#fdae61', '#ffff44']
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

scrobbles = get_scrobbles()
obsessions = get_obsessions(scrobbles, palette=colors)
loved_tracks = get_loved_tracks()

top_tags_data, top_tags_layout = top_tags_plot(color=colors[0])
top_artists_data, top_artists_layout = top_artists_plot(color=colors[1])
activity_data, activity_layout = activity_plot(scrobbles, obsessions, loved_tracks)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className='container text-center', children=[
    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            html.H1('Last Dash - interactive Last.fm dashboard'),
            html.Hr()
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='col-md-6', children=[
            dcc.Graph(
                id='top_tags',
                figure={
                    'data': top_tags_data,
                    'layout': top_tags_layout
                }
            )
        ]),
        html.Div(className='col-md-6', children=[
            dcc.Graph(
                id='top_artists',
                figure={
                    'data': top_artists_data,
                    'layout': top_artists_layout
                }
            )
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            dcc.Graph(
                id='activity',
                figure={
                    'data': activity_data,
                    'layout': activity_layout
                }
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)