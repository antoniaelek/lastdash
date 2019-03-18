# -*- coding: utf-8 -*-
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from data.plays_by_hour import get_plays_by_hour_data
from data.scrobbles import get_scrobbles_by_hour
from data.scrobbles import get_scrobbles
from data.artists import get_artists
from data.plays_by_artist import get_artists_plays_data
from plots.plays_by_artist import get_top_artists_plot
from plots.plays_by_hour import get_plays_by_hour

import pandas as pd


def top_artist_div(title, data, id, align_left=True):
    img_class = 'col-lg-6 col-md-12 justify-content-lg-end justify-content-center d-flex'  # right-tab behind'
    div_text_large_class = 'd-none d-lg-block col-lg-6 justify-content-lg-end text-left'  # left-tab in-front'
    if align_left is False:
        img_class = 'col-lg-6 col-md-12 justify-content-lg-start justify-content-center d-flex'  # left-tab behind'
        div_text_large_class = 'd-none d-lg-block col-lg-6 justify-content-lg-start text-right'  # right-tab in-front'

    div_img = html.Div(className=img_class, children=[
            html.Img(className='gridbox', src='https://lastfm-img2.akamaized.net/i/u/174s/c6f59c1e5e7240a4c0d427abd71f3dbb')
    ])
    div_text_large = html.Div(className=div_text_large_class, children=[
        html.H4(title, className='textbox'),
        html.H2("Apparently nobody")
    ])
    div_text_small = html.Div(className='d-xl-none col-md-12', children=[
        html.H3("Apparently nobody")
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

today = datetime.date.today()
min_date = scrobbles.index.min()[0]
max_date = today
periods = list(range(min_date.year,max_date.year))
periods += ['This year', 'This month', 'This week']
periods.reverse()

week_start = today - datetime.timedelta(days=7)
month_start = today - datetime.timedelta(days=today.day-1)

# print("Fetching top tags...")
# top_tags_trace, top_tags_layout = top_tags_plot(color=colors[0])
#
# print("Fetching top artists...")
# top_artists_trace, top_artists_layout = top_artists_plot(color=colors[1])


navbar = dbc.NavbarSimple(
    children=[
        #dbc.NavItem(dbc.NavLink("Top Artists", href="#")),
        dcc.Dropdown(
            id='year-input',
            options=[{'label': str(i), 'value': str(i)} for i in periods],
            value='This week',
            clearable=False,
            style={'bgcolor':'#f8f9fa','bordercolor':'#f8f9fa'}
        )
    ],
    brand="Last Dash",
    brand_href="#",
    sticky="top",
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className='text-center', children=[
    navbar,

    # Top artist
    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            html.H1('Your Last Dash', className='')
        ])
    ]),

    html.Div(id="content", children=[])
])


@app.callback(
    Output(component_id='content', component_property='children'),
    [Input(component_id='year-input', component_property='value')]
)
def update_output_div(input_value):
    if input_value == 'This week':
        scrobbles_selected = scrobbles[scrobbles['Timestamp'] >= pd.Timestamp(week_start)]
        intro = input_value
    elif input_value == 'This month':
        scrobbles_selected = scrobbles[scrobbles['Timestamp'] >= pd.Timestamp(month_start)]
        intro = input_value
    elif input_value == 'This year':
        scrobbles_selected = scrobbles[scrobbles['Year'] == int(today.year)]
        intro = input_value
    else:
        scrobbles_selected = scrobbles[scrobbles['Year'] == int(input_value)]
        intro = 'In ' + input_value

    # Top artist
    print("Filtering top artists...")
    top_artists = get_artists_plays_data(scrobbles_selected, artists, top_n=500)
    top_artists_div = top_artist_div("Your top artist", top_artists, "total")

    # Intro text
    print("Constructing intro text...")
    intro_text = top_artists_intro_text(intro, top_artists)

    top_artists_pie_trace, top_artists_pie_layout = get_top_artists_plot(top_artists)
    intro_text_div = html.Div(className='row palette-2', children=[
        html.Div(className='col-md-3', children=[]),
        html.Div(className='col-md-3', children=[
            dcc.Graph(figure={
                'data': top_artists_pie_trace,
                'layout': top_artists_pie_layout
            })
        ]),
        html.Div(className='col-md-3 centerflex', children=[
            html.H6(intro_text)
        ])
    ])

    # By hour data
    print("Grouping listening data by hour...")
    by_hour_data = get_plays_by_hour_data(scrobbles_selected)

    # By hour text
    by_hour_text = by_hour_intro_text(by_hour_data)
    by_hour_text_div = html.Div(className='row intro-text palette-3', children=[
        html.Div(className='col-md-2', children=[]),
        html.Div(className='col-md-8', children=[
            html.H6(by_hour_text + " Here's your scrobbling activity breakdown by hours...")
        ])
    ])

    # By hour graph
    by_hour_trace, by_hour_layout = get_plays_by_hour(by_hour_data)
    by_hour_div = html.Div(className='row palette-3', children=[
        html.Div(className='col-md-1', children=[]),
        html.Div(className='col-md-10', children=[
            dcc.Graph(figure={
                'data': by_hour_trace,
                'layout': by_hour_layout
            })
        ])
    ])

    return [top_artists_div, intro_text_div, by_hour_text_div, by_hour_div]


def by_hour_intro_text(by_hour_data):
    morning = int(by_hour_data.iloc[4:12].sum())
    afternoon = int(by_hour_data.iloc[12:20].sum())
    night = int(by_hour_data.iloc[20:24].append(by_hour_data.iloc[0:4]).sum())

    top_period = 'in the morning' if morning == max(morning, afternoon, night) else ''
    top_period = ' and in the afternoon' if afternoon == max(morning, afternoon, night) else top_period
    top_period = ' and during the night' if night == max(morning, afternoon, night) else top_period

    if top_period[:5] == " and ":
        top_period = top_period[5:]

    if morning+afternoon+night == 0:
        return "You didn't scrobble anything at all."
    else:
        top_percent = round((max(morning, afternoon, night) / (morning+afternoon+night) * 100))

    return "You scrobbled most tracks ({}%) {}.".format(top_percent, top_period)


def top_artists_intro_text(period, top_artists):
    intro_text = '{}, there were no scrobbles.'.format(period)
    if len(top_artists['PlayCount']) > 0:
        overall_percent_top_1 = int(round(top_artists['PlayCount'].iloc[-1] / top_artists.sum().PlayCount * 100))
        intro_text = "{}, {}% of your scrobbles were by {}.".format(period, overall_percent_top_1, top_artists.index[-1])
    if len(top_artists['PlayCount']) > 1:
        overall_percent_top_2 = int(round(top_artists['PlayCount'].iloc[-2] / top_artists.sum().PlayCount * 100))
        intro_text += " Another {}% were by {}".format(overall_percent_top_2, top_artists.index[-2])

        if len(top_artists['PlayCount']) > 2:
            overall_percent_top_3 = int(round(top_artists['PlayCount'].iloc[-3] / top_artists.sum().PlayCount * 100))
            intro_text += ", and {}% were by {}.".format(overall_percent_top_3, top_artists.index[-3])
        else:
            intro_text += "."
    return intro_text


if __name__ == '__main__':
    app.run_server(debug=True)
