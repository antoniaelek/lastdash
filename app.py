# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from plots.tags import top_tags_plot

top_tags_data, top_tags_layout = top_tags_plot()

external_stylesheets = [#'https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(className='container text-center', children=[
    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            html.H1('Last Dash - interactive Last.fm dashboard'),
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
            dcc.Graph(
                id='top_tags',
                figure={
                    'data': [top_tags_data],
                    'layout': top_tags_layout
                }
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)