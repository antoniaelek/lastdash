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

    artists = (get_artists_plays(scrobbles).merge(artists[['URL', 'ImageURL']],
                                                  how='left',
                                                  left_index=True,
                                                  right_index=True))
    return artists.head(top_n).sort_values('PlayCount')


def get_artists_plays(scrobbles):
    if len(scrobbles) == 0:
        return get_artists_plays_by_date(scrobbles).reset_index().groupby('Artist').sum()

    artists_play_counts = get_artists_plays_by_date(scrobbles)
    return (artists_play_counts.reset_index()
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
