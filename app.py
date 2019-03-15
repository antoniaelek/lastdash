# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from data.scrobbles import get_scrobbles
from data.artists import get_artists

from plots.plays_by_artist import get_artists_plays_at_work_plot, get_artists_plays_data
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

    div_img = html.Div(className=img_class, children=[
            html.Img(className='gridbox', src='https://lastfm-img2.akamaized.net/i/u/174s/c6f59c1e5e7240a4c0d427abd71f3dbb')
    ])
    div_text_large = html.Div(className=div_text_large_class, children=[
        html.H4(title, className='textbox'),
        html.H2("No Scrobbles")
    ])
    div_text_small = html.Div(className='d-xl-none col-md-12', children=[
        html.H3("No Scrobbles")
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

# print("Fetching top tags...")
# top_tags_trace, top_tags_layout = top_tags_plot(color=colors[0])
#
# print("Fetching top artists...")
# top_artists_trace, top_artists_layout = top_artists_plot(color=colors[1])


navbar = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink("Top Artists", href="#")),
        dcc.Dropdown(
            id='year-input',
            options=[{'label': str(i), 'value': str(i)} for i in scrobbles['Year'].unique()],
            value='2019',
            clearable=False,
            style={'bgcolor':'#f8f9fa','bordercolor':'#f8f9fa'}
        ),

        # dbc.DropdownMenu(
        #    nav=True,
        #    in_navbar=True,
        #    label="Year",
        #    children=[
        #        dbc.DropdownMenuItem("Entry 1"),
        #        dbc.DropdownMenuItem("Entry 2"),
        #        dbc.DropdownMenuItem("Entry 3"),
        #    ],
        #  ),
    ],
    brand="Last Dash",
    brand_href="#",
    sticky="top",
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className='text-center', children=[
    navbar,

    # Top artist at work, on weekends and late at night
    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            html.H1('Your top artists', className='')
        ])
    ]),

    html.Div(id="content", children=[])
])

@app.callback(
    Output(component_id='content', component_property='children'),
    [Input(component_id='year-input', component_property='value')]
)
def update_output_div(input_value):
    scrobbles_selected = scrobbles[scrobbles['Year'] == int(input_value)]

    print("Fetching top artists overall...")
    overall = get_artists_plays_data(scrobbles_selected, artists)
    overall_div = top_artist_div("Overall", overall, "total")

    print("Fetching top artists at work...")
    at_work = get_artists_plays_at_work_data(scrobbles_selected, artists)
    at_work_div = top_artist_div("At Work", at_work, "top-work", align_left=False)

    print("Fetching top late night artists...")
    late_night = get_artists_plays_late_at_night(scrobbles_selected, artists)
    late_night_div = top_artist_div("Late At Night", late_night, "top-late-night")

    print("Fetching top weekend artists...")
    weekends = get_artists_plays_on_weekends(scrobbles_selected, artists)
    weekends_div = top_artist_div("On Weekends", weekends, "top-weekends", align_left=False)

    return [overall_div, at_work_div, late_night_div, weekends_div]


if __name__ == '__main__':
    app.run_server(debug=True)
