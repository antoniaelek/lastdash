def get_plays_by_hour_data(scrobbles):
    return scrobbles[['Hour', 'PlayCount']].groupby('Hour').sum().reindex(list(range(0, 24)), fill_value=0)
