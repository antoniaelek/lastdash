import plotly.graph_objs as go


def get_plays_by_hour(data, color='#000', color_grid='#777', width=3, font_family='Arial'):
    trace = go.Scatter(
        x=data.index,
        y=data['PlayCount'],
        mode='lines',
        hoverinfo='none',
        fill='tozeroy',
        line=dict(
            shape='spline',
            color=color,
            width=width
        )
    )

    layout = go.Layout(
        xaxis=dict(
            mirror='ticks',
            showticklabels=True,
            zeroline=False,
            showline=False,
            gridcolor=color_grid,
            range=[0, 24],
            tickmode='array',
            tickvals=list(range(0,24)),
            tickfont=dict(
                color=color_grid
            )
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            range=[0-max(data['PlayCount'])*0.1, max(data['PlayCount'])*1.1],
            ticks='',
            showticklabels=False
        ),
        font=dict(
            family=font_family
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return [trace], layout
