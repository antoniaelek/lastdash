import plotly.graph_objs as go
from data.plays_by_artist import get_artists_plays_at_work
from data.plays_by_artist import get_artists_plays_weekends
from data.plays_by_artist import get_artists_plays_late_night
import datetime


def get_artists_plays_at_work_data(scrobbles, artists, top_n=8):
    start = scrobbles.index.min()[0]
    end = scrobbles.index.max()[0]

    # last_monday = end - datetime.timedelta(days=end.weekday())
    # start = last_monday

    artists = (get_artists_plays_at_work(scrobbles, start, end)
        .merge(artists[['URL', 'ImageURL']], how='left', left_index=True, right_index=True))
    artists.head()

    return artists.head(top_n).sort_values('PlayCount')


def get_artists_plays_on_weekends(scrobbles, artists, top_n=8):
    start = scrobbles.index.min()[0]
    end = scrobbles.index.max()[0]

    # last_saturday = end - datetime.timedelta(days=end.weekday())
    # start = last_saturday - datetime.timedelta(days=3)
    # end = last_saturday + datetime.timedelta(days=1)

    artists = (get_artists_plays_weekends(scrobbles, start, end)
        .merge(artists[['URL', 'ImageURL']], how='left', left_index=True, right_index=True))
    artists.head()

    return artists.head(top_n).sort_values('PlayCount')


def get_artists_plays_late_at_night(scrobbles, artists, top_n=8):
    start = scrobbles.index.min()[0]
    end = scrobbles.index.max()[0]

    # last_monday = end - datetime.timedelta(days=end.weekday())
    # start = last_monday

    artists = (get_artists_plays_late_night(scrobbles, start, end)
        .merge(artists[['URL', 'ImageURL']], how='left', left_index=True, right_index=True))
    artists.head()

    return artists.head(top_n).sort_values('PlayCount')


def get_artists_plays_at_work_plot(top, color=None, title_size=28):
    data = go.Bar(
        x=top['PlayCount'],
        y=top.index,
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
