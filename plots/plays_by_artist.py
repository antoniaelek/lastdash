import plotly.graph_objs as go


def get_artists_plays_at_work_plot(data, color=None, title_size=28):
    data = go.Bar(
        x=data['PlayCount'],
        y=data.index,
        orientation='h'
    )

    line = {}
    if color is not None:
        line['color'] = color

    layout = go.Layout(
        title='Top artists played at work',
        titlefont=dict(size=title_size),
        showlegend=False
    )

    return [data], layout
