import datetime


def get_artists_plays_by_date(scrobbles):
    return (scrobbles[['PlayCount']]
            .groupby(['Date', 'Artist'])
            .sum()
            .reset_index()
            .sort_values(['Date', 'PlayCount'], ascending=False)
            .set_index('Date'))


def get_artists_plays_data(scrobbles, artists, top_n=8):
    if len(scrobbles) == 0:
        ret = get_artists_plays(scrobbles)
        ret['ImageURL'] = ''
        ret['URL'] = ''
        return ret

    start = scrobbles.index.min()[0]
    end = scrobbles.index.max()[0]

    artists = (get_artists_plays(scrobbles, start, end)
        .merge(artists[['URL', 'ImageURL']], how='left', left_index=True, right_index=True))
    artists.head()

    return artists.head(top_n).sort_values('PlayCount')


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


def merge_artists_plays(scrobbles, summed, artists, top_n=8):
    if len(scrobbles) == 0:
        ret = summed
        ret['ImageURL'] = ''
        ret['URL'] = ''
        return ret

    result = summed.merge(artists[['URL', 'ImageURL']], how='left', left_index=True, right_index=True)

    return result.head(top_n).sort_values('PlayCount')


def get_artists_plays_at_workdays(scrobbles, artists, period_start=None, period_end=None, top_n=8):
    filtered = scrobbles[scrobbles['IsWeekend'] == False]
    summed = get_artists_plays(filtered, period_start, period_end)
    return merge_artists_plays(scrobbles, summed, artists, top_n)


def get_artists_plays_weekends(scrobbles, artists, period_start=None, period_end=None, top_n=8):
    filtered = scrobbles[(scrobbles['IsWeekend'] == True)]
    summed = get_artists_plays(filtered, period_start, period_end)
    return merge_artists_plays(scrobbles, summed, artists, top_n)


def get_artists_plays_morning(scrobbles, artists, period_start=None, period_end=None, top_n=8):
    filtered = scrobbles[(scrobbles['Hour'] >= 4) & (scrobbles['Hour'] < 12)]
    summed = get_artists_plays(filtered, period_start, period_end)
    return merge_artists_plays(scrobbles, summed, artists, top_n)


def get_artists_plays_afternoon(scrobbles, artists, period_start=None, period_end=None, top_n=8):
    filtered = scrobbles[(scrobbles['Hour'] >= 12) & (scrobbles['Hour'] < 20)]
    summed = get_artists_plays(filtered, period_start, period_end)
    return merge_artists_plays(scrobbles, summed, artists, top_n)


def get_artists_plays_night(scrobbles, artists, period_start=None, period_end=None, top_n=8):
    filtered = scrobbles[(scrobbles['Hour'] >= 20) | (scrobbles['Hour'] < 4)]
    summed = get_artists_plays(filtered, period_start, period_end)
    return merge_artists_plays(scrobbles, summed, artists, top_n)