import plotly.graph_objs as go


def get_top_artists_plot(top_artists, color=None, title_size=28):
    data = []
    labels = []

    overall_percent_top_1 = 100
    overall_name_top_1 = 'No one'
    if len(top_artists['PlayCount']) > 0:
        overall_percent_top_1 = int(round(top_artists['PlayCount'].iloc[-1] / top_artists.sum().PlayCount * 100))
        overall_name_top_1 = top_artists.index[-1]

    data = data + [overall_percent_top_1]
    labels = labels + [overall_name_top_1]

    if len(top_artists['PlayCount']) > 1:
        data += [int(round(top_artists['PlayCount'].iloc[-2] / top_artists.sum().PlayCount * 100))]
        labels += [top_artists.index[-2]]

    if len(top_artists['PlayCount']) > 2:
        data += [int(round(top_artists['PlayCount'].iloc[-3] / top_artists.sum().PlayCount * 100))]
        labels += [top_artists.index[-3]]

    if sum(data) < 100:
        data += [(100 - sum(data))]
        labels += ['others']

    colors = ['#fff', '#eee', '#ddd', '#ccc']

    trace = go.Pie(
        labels=labels,
        values=data,
        hoverinfo='label+percent',
        textinfo='none',
        marker=dict(colors=colors, line=dict(width=0))
    )

    layout = go.Layout(
        # title='Top artists played at work',
        # titlefont=dict(size=title_size),
        showlegend=False,
        # margin=go.layout.Margin(
        #     l=0,
        #     r=0,
        #     b=0,
        #     t=10,
        #     pad=0
        # ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return [trace], layout
