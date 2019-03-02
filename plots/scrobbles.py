import plotly.graph_objs as go


def activity_plot(scrobbles, obsessions, loved_tracks,
                  color_scrobbles=None, color_obsessions=None, color_loved_tracks=None,
                  title_size=28):
    loved_by_date = loved_tracks[['Timestamp', 'Date']].groupby('Date').count()
    loved_by_date.rename(columns={'Timestamp': 'Count'}, inplace=True)

    line_loved_tracks = {}
    if color_loved_tracks is not None:
        line_loved_tracks['color'] = color_loved_tracks

    loved_tracks_trace = go.Bar(
        x=loved_by_date.index.values,
        y=loved_by_date['Count'],
        name="Loved tracks",
        opacity=0.8,
        yaxis='y2',
        hovertext=' loved tracks',
        hoverinfo='y+text')

    scrobbles_by_date = scrobbles[['Timestamp', 'Date']].groupby('Date').count()
    scrobbles_by_date.rename(columns={'Timestamp': 'Count'}, inplace=True)

    line_scrobbles = {}
    if color_scrobbles is not None:
        line_scrobbles['color'] = color_scrobbles

    scrobbles_trace = go.Scatter(
        x=scrobbles_by_date.index.values,
        y=scrobbles_by_date['Count'],
        name="Scrobbles",
        fill='tozeroy',
        line=line_scrobbles,
        opacity=0.8,
        yaxis='y1',
        hovertext=' scrobbled tracks',
        hoverinfo='y+text')

    line_obsessions = {}
    if color_obsessions is not None:
        line_obsessions['color'] = color_obsessions

    obsessions_trace = go.Bar(
        x=obsessions.index.values,
        y=obsessions['Cnt'],
        name='Obsessions',
        text='<a style="color:inherit" href="' + obsessions['URL'] + '">' + obsessions['Artist'] + ': ' + obsessions[
            'Track'] + "</a>",
        opacity=0.8,
        yaxis='y3',
        hoverinfo='y+text')

    layout = dict(
        showlegend=False,
        title='Activity',
        titlefont=dict(size=title_size),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                         label='past week',
                         step='day',
                         stepmode='backward'),
                    dict(count=1,
                         label='past month',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='past 6 months',
                         step='month',
                         stepmode='backward'),
                    dict(count=12,
                         label='past year',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            type='date'
        ),
        yaxis=dict(
            title='Scrobbles', domain=[0, 0.33]
        ),
        yaxis2=dict(
            title='Loved tracks', domain=[0.33, 0.66]
        ),
        yaxis3=dict(
            title='Obsessions', domain=[0.66, 1]
        ),
        legend=dict(
            traceorder='reversed'
        )
    )

    data = [scrobbles_trace, loved_tracks_trace, obsessions_trace]
    return data, layout
