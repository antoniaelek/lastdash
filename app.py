# -*- coding: utf-8 -*-
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from data.plays_by_hour import get_plays_by_hour_data
from data.plays_by_tag import get_tags
from data.plays_by_track import get_tracks_plays_data
from data.scrobbles import get_scrobbles
from data.artists import get_artists
from data.plays_by_artist import get_artists_plays_data
from plots.plays_by_artist import get_top_artists_plot
from plots.plays_by_hour import get_plays_by_hour
from plots.plays_by_tag import top_tags_plot

import pandas as pd


def single_top_div(title, data, id, align_left=True):
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
            html.Img(className='gridbox', src=data.iloc[-1].ImageURL.replace('300x300', '450x450'))
        ])

        div_text_large = html.Div(className=div_text_large_class, children=[
            html.H4(title, className='textbox'),
            html.H2(data.index[-1], className=''),
            html.H4('{} plays'.format(data.iloc[-1].PlayCount), className="")
        ])
        div_text_small = html.Div(className='d-lg-none col-md-12 pad-bottom', children=[
            html.H3(data.index[-1], className=''),
            html.H4('{} plays'.format(data.iloc[-1].PlayCount), className="")
        ])

    if align_left:
        div = html.Div(className='row centerbox half-screen palette palette-1', id=id,
                       children=[div_title_small, div_img, div_text_large, div_text_small])
    else:
        div = html.Div(className='row centerbox half-screen palette palette-1', id=id,
                       children=[div_title_small, div_text_large, div_img, div_text_small])

    return div


##############################################
#                                            #
#                  M A I N                   #
#                                            #
##############################################

username = 'muser1901'
avatar = 'https://lastfm-img2.akamaized.net/i/u/6e51680a8855f69fbb8dcd65dffdb34a.png'

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
periods = ['Overall']
periods += list(range(min_date.year, max_date.year))
periods += ['This year', 'This month', 'This week']
periods.reverse()

week_start = today - datetime.timedelta(days=7)
month_start = today - datetime.timedelta(days=today.day - 1)

navbar = dbc.NavbarSimple(
    children=[
        dcc.Dropdown(
            id='year-input',
            options=[{'label': str(i), 'value': str(i)} for i in periods],
            value='This week',
            clearable=False,
            style={'bgcolor': '#f8f9fa', 'bordercolor': '#f8f9fa'}
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
    html.Div(className='row palette palette-0 half-screen centerbox', children=[
        html.Div(className='col-md-12 pad-sm-b', children=[
            html.Img(className='gridbox-xs avatar', src=avatar),
            html.H2('Your life in music', className='inverted-text'),
            html.H5(username + ', here is your scrobbles dashboard', className='inverted-text')
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
    elif input_value == 'Overall':
        scrobbles_selected = scrobbles
        intro = input_value
    else:
        scrobbles_selected = scrobbles[scrobbles['Year'] == int(input_value)]
        intro = 'In ' + input_value

    if len(scrobbles_selected) == 0:
        return [html.Div(className='row palette palette-1 half-screen', children=[
            html.Div(className='col-md-12 valign', children=[
                html.H6(intro + ", you didn't scrobble anything.")
            ]),
        ])]

    # Top artist
    print("Filtering top artists...")
    top_artists = get_artists_plays_data(scrobbles_selected, artists, top_n=500)
    top_artists_div = single_top_div("Your top artist", top_artists, "total-artist")

    # Top artists pie
    print("Top artists pie chart...")
    top_artists_pie_trace, top_artists_pie_layout = get_top_artists_plot(top_artists)
    intro_text_div = html.Div(className='row palette palette-2 pad-sm-b', children=[
        html.Div(className='col-lg-1 col-md-2', children=[]),
        html.Div(className='col-lg-5 col-md-8', children=[
            dcc.Graph(figure={
                'data': top_artists_pie_trace,
                'layout': top_artists_pie_layout
            })
        ]),
        html.Div(className='col-sm-2 d-lg-none', children=[]),
        html.Div(className='col-md-2 d-lg-none', children=[]),
        html.Div(className='col-lg-5 col-md-8 col-sm-12 centerflex', children=[
            html.H6(children=top_artists_intro_text(intro, top_artists, 'inverted-highlighted-text'), className='inverted-text')
        ])
    ])

    # Top track
    print("Filtering top tracks...")
    top_tracks = get_tracks_plays_data(scrobbles_selected, top_n=500)
    top_tracks_div = single_top_div("Your top track", top_tracks, "total-track", align_left=False)

    # By hour data
    print("Grouping listening data by hour...")
    by_hour_data = get_plays_by_hour_data(scrobbles_selected)

    # By hour text
    morning = int(by_hour_data.iloc[4:12].sum())
    afternoon = int(by_hour_data.iloc[12:19].sum())
    night = int(by_hour_data.iloc[19:].append(by_hour_data.iloc[0:4]).sum())
    by_hour_text_div = html.Div(className='row intro-text palette palette-3', children=[
        html.Div(className='col-md-2', children=[]),
        html.Div(className='col-md-8', children=[
            html.H6(children=by_hour_intro_text(morning, afternoon, night, "highlighted-text")),
            html.H6("Here's how you scrobbled by hours.")
        ])
    ])

    # By hour graph
    by_hour_trace, by_hour_layout = get_plays_by_hour(by_hour_data, color='#333')
    by_hour_div = html.Div(className='row palette palette-3', children=[
        html.Div(className='col-lg-12 col-md-12', children=[
            dcc.Graph(figure={
                'data': by_hour_trace,
                'layout': by_hour_layout
            })
        ])
    ])

    # Total scrobbles
    morning_label = str(morning) if morning < 1000 else str(round(float(morning/1000),1)) + 'k'
    afternoon_label = str(afternoon) if afternoon < 1000 else str(round(float(afternoon/1000),1)) + 'k'
    night_label = str(night) if night < 1000 else str(round(float(night/1000),1)) + 'k'

    total_scrobbles_text_div = html.Div(className='row palette palette-3 pad-sm-b', children=[
        html.Div(className='col-md-4', children=[
            html.H1(morning_label),
            html.H6("Morning scrobbles")
        ]),
        html.Div(className='col-md-4', children=[
            html.H1(afternoon_label),
            html.H6("Afternoon scrobbles")
        ]),
        html.Div(className='col-md-4', children=[
            html.H1(night_label),
            html.H6("Night scrobbles")
        ])
    ])

    # Top tags
    print("Fetching top tags...")
    top_tags_data = get_tags(scrobbles_selected)
    top_tags_trace, top_tags_layout = top_tags_plot(top_tags_data)
    top_tags_div = html.Div(className='row palette palette-4 pad-sm-b inverted-text', children=[
        html.Div(className='col-lg-1 col-md-12', children=[]),
        html.Div(className='col-lg-5 col-md-12', children=[
            dcc.Graph(figure={
                'data': top_tags_trace,
                'layout': top_tags_layout
            })
        ]),
        html.Div(className='col-lg-5 col-md-12 valign', children=[
            html.H6(children=top_tags_text(top_tags_data, 'highlighted-text'))
        ])
    ])

    return [top_artists_div, intro_text_div, top_tracks_div, by_hour_text_div, by_hour_div, total_scrobbles_text_div, top_tags_div]


def top_tags_text(data, highlight_class):
    percents = data['Percent'].unique()
    percents_pretty = data['PercentPretty'].unique()
    spans = []
    if len(percents) > 0:
        top_tags = get_tags_by_percent(data, percents[0])
        spans += tag_spans(percents_pretty[0], highlight_class, top_tags, 'Your top tag was', 'Your top tags were')

    if len(percents) > 1:
        spans += [html.Span(" ")]
        top_tags_2 = get_tags_by_percent(data, percents[1])
        spans += tag_spans(percents_pretty[1], highlight_class, top_tags_2, 'Next was', 'Next were')

    return spans


def tag_spans(percent_pretty, highlight_class, top_tags, intro_singular, intro_plural):
    intro_singular = intro_singular if intro_singular[-1] == ' ' else intro_singular + ' '
    intro_plural = intro_plural if intro_plural[-1] == ' ' else intro_plural + ' '
    spans = []
    if len(top_tags) > 1:
        spans += [html.Span(intro_plural)]
        for tag in top_tags[:-1]:
            spans += [html.Span(tag, className=highlight_class)]
            spans += [html.Span(', ')]
        spans = spans[:-1]
        spans += [html.Span(" and ")]
        spans += [html.Span(top_tags[-1], className=highlight_class)]
    else:
        spans += [html.Span(intro_singular)]
        spans += [html.Span(top_tags[0], className=highlight_class)]
    spans += [html.Span(', which appeared in ')]
    spans += [html.Span(percent_pretty, className=highlight_class)]
    spans += [html.Span(' of your scrobbles.')]
    return spans


def get_tags_by_percent(data, percent):
    max_data = data[data['Percent'] == percent].head(8)
    if len(max_data) == 0:
        return None

    return list(max_data.index)


def by_hour_intro_text(morning, afternoon, night, highlight_class):
    top_period = 'in the morning' if morning == max(morning, afternoon, night) else ''
    top_period = ' and in the afternoon' if afternoon == max(morning, afternoon, night) else top_period
    top_period = ' and during the night' if night == max(morning, afternoon, night) else top_period

    if top_period[:5] == " and ":
        top_period = top_period[5:]

    if morning + afternoon + night == 0:
        return [html.Span("You didn't scrobble anything at all.")]

    top_percent = round((max(morning, afternoon, night) / (morning + afternoon + night) * 100))

    spans = []
    spans += [html.Span('You scrobbled most tracks ')]
    spans += [html.Span(f'({top_percent}%) {top_period}', className=highlight_class)]
    spans += [html.Span('.')]
    return spans


def top_artists_intro_text(period, top_artists, highlight_class):
    if len(top_artists['PlayCount']) == 0:
        return ['{}, there were no scrobbles.'.format(period)]

    spans = []
    if len(top_artists['PlayCount']) > 0:
        overall_percent_top_1 = int(round(top_artists['PlayCount'].iloc[-1] / top_artists.sum().PlayCount * 100))
        spans += [html.Span('{}, '.format(period))]
        spans += [html.Span(f'{overall_percent_top_1}%', className=highlight_class)]
        spans += [html.Span(' of your scrobbles were by ')]
        spans += [html.Span(top_artists.index[-1], className=highlight_class)]
        spans += [html.Span('.')]

    if len(top_artists['PlayCount']) > 1:
        overall_percent_top_2 = int(round(top_artists['PlayCount'].iloc[-2] / top_artists.sum().PlayCount * 100))
        spans += [html.Span(' Another ')]
        spans += [html.Span(f'{overall_percent_top_2}%', className=highlight_class)]
        spans += [html.Span(' were by ')]
        spans += [html.Span(top_artists.index[-2], className=highlight_class)]
        spans += [html.Span('.')]

    if len(top_artists['PlayCount']) > 2:
        overall_percent_top_3 = int(round(top_artists['PlayCount'].iloc[-3] / top_artists.sum().PlayCount * 100))
        spans += [html.Span(' Further ')]
        spans += [html.Span(f'{overall_percent_top_3}%', className=highlight_class)]
        spans += [html.Span(' were by ')]
        spans += [html.Span(top_artists.index[-3], className=highlight_class)]
        spans += [html.Span('.')]

    return spans


if __name__ == '__main__':
    app.run_server(debug=False)
