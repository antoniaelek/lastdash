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


def top_artist_div(title, data, id, align_left=True):
    div_img = html.Div(className='col-lg-6')
    div_text_large = html.Div(className='col-lg-6 d-md-none', children=[
        html.H1(title),
        html.H2("no scrobbles", className="box-title box-title-lg")
    ])
    div_text_small = html.Div(className='d-xl-none col-md-12', children=[
        html.H2("no scrobbles", className="box-title")
    ])
    div_title_small = html.Div(className='d-xl-none col-md-12', children=[
        html.H1(title)
    ])

    if len(data) > 0:
        div_img = html.Div(className='col-xl-6', children=[
            html.Img(className='gridbox', src=data.at[data.index[-1], 'ImageURL'].replace('300x300', '450x450'))
        ])
        div_text_large = html.Div(className='d-none d-xl-block col-xl-6', children=[
            html.H1(title),
            html.H2(data.index[-1], className="box-title box-title-lg"),
            html.H4('{} plays'.format(data.at[data.index[-1], 'PlayCount']),
                    className="box-subtitle box-subtitle-lg")
        ])
        div_text_small = html.Div(className='d-xl-none col-md-12', children=[
            html.H2(data.index[-1], className="box-title"),
            html.H4('{} plays'.format(data.at[data.index[-1], 'PlayCount']),
                    className="box-subtitle")
        ])

    if align_left:
        div = html.Div(className='row centerbox full-screen', id=id,
                       children=[div_title_small, div_img, div_text_large, div_text_small])
    else:
        div = html.Div(className='row centerbox full-screen', id=id,
                       children=[div_title_small, div_text_large, div_img, div_text_small])

    return div


##############################################
#                                            #
#                  M A I N                   #
#                                            #
##############################################

colors = ['#d7191c', '#2b83ba', '#abdda4', '#fdae61', '#ffff44']
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
                        '/static/custom.css']

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

work_div = top_artist_div("At Work", top_at_work, "top-work")
weekends_div = top_artist_div("On Weekends", top_weekends, "top-weekends", align_left=False)
late_night_div = top_artist_div("Late At Night", top_late_night, "top-late-night")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className='text-center', children=[
    # Title
    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            html.H1('Last Dash', className="")
        ])
    ]),

    # Top artist at work, on weekends and late at night
    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            html.H2('Your top artists', className="display-3")
        ])
    ]),
    work_div,
    weekends_div,
    late_night_div
])

if __name__ == '__main__':
    app.run_server(debug=True)
