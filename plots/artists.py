from data.artists import get_artists
import plotly.graph_objs as go


def _get_top_artists_for_plot(artists, top_n=8):
    top_artists = artists.head(top_n)
    top_artists = top_artists.sort_values(by=['Name'], inplace=False, ascending=False)
    top_artists = top_artists.iloc[-3:].append(top_artists.iloc[:-3])
    top_artists = top_artists.append(top_artists.iloc[0])
    return top_artists


def top_artists_plot(filename='csv/artists.csv', top_n=8, color=None, title_size=28):
    artists = get_artists(filename=filename)
    top_artists = _get_top_artists_for_plot(artists=artists, top_n=top_n)
    line = {}
    if color is not None:
        line['color'] = color
    data = go.Scatterpolar(
      r=top_artists['Count'],
      theta='<a style="color:inherit" href="' + top_artists['URL'] + '">' + top_artists['Name'] + '</a>',
      fill='toself',
      line=line,
      hovertext=top_artists['PercentPretty'] + ' of all played artists',
      hoverinfo='text'
    )
    layout = go.Layout(
        title='Top artists',
        titlefont=dict(size=title_size),
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, artists.iloc[0]['Count']]
            )
        ),
        showlegend=False
    )
    return data, layout
