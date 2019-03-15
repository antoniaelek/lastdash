import datetime
import numpy as np

def get_artists_plays_by_date(scrobbles):
    return (scrobbles[['PlayCount']]
            .groupby(['Date', 'Artist'])
            .sum()
            .reset_index()
            .sort_values(['Date', 'PlayCount'], ascending=False)
            .set_index('Date'))


def get_artists_plays(scrobbles, period_start=None, period_end=None):
    if len(scrobbles) == 0:
        return get_artists_plays_by_date(scrobbles).reset_index().groupby('Artist').sum()

    if period_start is None:
        period_start = scrobbles.index.min()[0]

    if period_end is None:
        period_end = scrobbles.index.max()[0] + datetime.timedelta(days=1)

    artists_play_counts = get_artists_plays_by_date(scrobbles)
    return (artists_play_counts[(artists_play_counts.index >= period_start) & (artists_play_counts.index <= period_end)]
            .reset_index()
            .groupby('Artist')
            .sum()
            .sort_values('PlayCount', ascending=False))


def get_artists_plays_at_work(scrobbles, period_start=None, period_end=None):
    at_work = scrobbles[(scrobbles['IsWeekend'] == False) & (scrobbles['Hour'] > 6) & (scrobbles['Hour'] < 19)]
    return get_artists_plays(at_work, period_start, period_end)


def get_artists_plays_weekends(scrobbles, period_start=None, period_end=None):
    weekends = scrobbles[(scrobbles['IsWeekend'] == True)]
    return get_artists_plays(weekends, period_start, period_end)


def get_artists_plays_late_night(scrobbles, period_start=None, period_end=None):
    late_night = scrobbles[(scrobbles['Hour'] < 5) | (scrobbles['Hour'] > 20)]
    return get_artists_plays(late_night, period_start, period_end)
