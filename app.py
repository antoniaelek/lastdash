# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from data.scrobbles import get_scrobbles
from data.artists import get_artists

from plots.plays_by_artist import get_artists_plays_at_work_plot
from plots.plays_by_artist import get_artists_plays_at_work_data
from plots.plays_by_artist import get_artists_plays_late_at_night
from plots.plays_by_artist import get_artists_plays_on_weekends
from plots.tags import top_tags_plot
from plots.artists import top_artists_plot


def top_artist_div(title, data, id, align_left=True):
    img_class = 'col-lg-6 col-md-12 justify-content-lg-end justify-content-center d-flex'  # right-tab behind'
    div_text_large_class = 'd-none d-lg-block col-lg-6 justify-content-lg-end text-left'  # left-tab in-front'
    if align_left is False:
        img_class = 'col-lg-6 col-md-12 justify-content-lg-start justify-content-center d-flex'  # left-tab behind'
        div_text_large_class = 'd-none d-lg-block col-lg-6 justify-content-lg-start text-right'  # right-tab in-front'

    div_img = html.Div(className=img_class)
    div_text_large = html.Div(className=div_text_large_class, children=[
        html.H4(title),
        html.H2("no scrobbles")
    ])
    div_text_small = html.Div(className='d-xl-none col-md-12', children=[
        html.H3("no scrobbles")
    ])
    div_title_small = html.Div(className='d-lg-none col-md-12 pad', children=[
        html.H3(title, className="textbox")
    ])

    if len(data) > 0:
        div_img = html.Div(className=img_class, children=[
            html.Img(className='gridbox', src=data.at[data.index[-1], 'ImageURL'].replace('300x300', '450x450'))
        ])

        div_text_large = html.Div(className=div_text_large_class, children=[
            html.H4(title, className='textbox'),
            html.H2(data.index[-1], className=''),
            html.H4('{} plays'.format(data.at[data.index[-1], 'PlayCount']), className="")
        ])
        div_text_small = html.Div(className='d-lg-none col-md-12 pad-bottom', children=[
            html.H3(data.index[-1], className=''),
            html.H4('{} plays'.format(data.at[data.index[-1], 'PlayCount']), className="")
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
                        '/static/custom.css',
                        'dbc.themes.BOOTSTRAP']

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

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Top Artists", href="#")),
#        dbc.DropdownMenu(
#            nav=True,
#            in_navbar=True,
#            label="Menu",
#            children=[
#                dbc.DropdownMenuItem("Entry 1"),
#                dbc.DropdownMenuItem("Entry 2"),
#                dbc.DropdownMenuItem(divider=True),
#                dbc.DropdownMenuItem("Entry 3"),
#            ],
#        ),
    ],
    brand="Last Dash",
    brand_href="#",
    sticky="top",
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className='text-center', children=[
    # Title
    navbar,

    # html.Div(className='row', children=[
    #     html.Div(className='col-md-12', children=[
    #         html.H1('Last Dash', className="")
    #     ])
    # ]),

    # Top artist at work, on weekends and late at night
    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            html.H1('Your top artists', className='')
        ])
    ]),
    work_div,
    weekends_div,
    late_night_div
])

if __name__ == '__main__':
    app.run_server(debug=True)
