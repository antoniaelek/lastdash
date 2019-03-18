import plotly.graph_objs as go


def get_plays_by_hour(data):
    trace = go.Scatter(
        x=data.index,
        y=data['PlayCount'],
        mode='lines',
        hoverinfo='y',
        line=dict(
            shape='spline'
        )
    )

    layout = go.Layout(
        xaxis=dict(
            mirror='ticks',
            showticklabels=True,
            zeroline=False,
            showline=False,
            range=[0, 24],
            tickmode='array',
            tickvals=list(range(0,24))
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            range=[0-max(data['PlayCount'])*0.1, max(data['PlayCount'])*1.1],
            ticks='',
            showticklabels=False
        )
    )

    return [trace], layout
