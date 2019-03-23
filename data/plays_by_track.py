def get_tracks_plays_data(scrobbles, top_n=8):
    return get_tracks_plays(scrobbles).head(top_n).sort_values('PlayCount')


def get_tracks_plays(scrobbles):
    if len(scrobbles) == 0:
        return get_tracks_plays_by_date(scrobbles).reset_index().groupby('Track').sum()

    track_play_counts = get_tracks_plays_by_date(scrobbles)
    return (track_play_counts.reset_index()
                             .groupby(['Track','URL','ImageURL'])
                             .sum()
                             .sort_values('PlayCount', ascending=False)
                             .reset_index()
                             .set_index('Track'))


def get_tracks_plays_by_date(scrobbles):
    return (scrobbles.groupby(['Date', 'Track', 'URL','ImageURL'])
                     .sum()
                     .reset_index()
                     .sort_values(['Date', 'PlayCount'], ascending=False)
                     .set_index('Date'))
