import pandas as pd


def get_tags(scrobbles, filename='csv/artists-tags.csv'):
    artist_tags = (pd.read_csv(filename,
                               names=['Artist', 'ArtistURL', 'ArtistImageURL', 'Weight', 'Tag', 'TagURL'],
                               header=None,
                               sep='\t'))

    df = pd.merge(artist_tags, scrobbles.reset_index(), on='Artist')
    df['Score'] = df['PlayCount']  # * df['Weight']
    df = (df[['Tag', 'TagURL', 'Date', 'Timestamp', 'Score']].groupby(['Date', 'Tag', 'TagURL'])
                                                             .sum()
                                                             .sort_values(by=['Date', 'Score'], ascending=False))
    df = (df.reset_index()
            .groupby(['Tag', 'TagURL'])
            .sum().sort_values(by=['Score'], ascending=False)
            .reset_index()
            .set_index('Tag')
            .rename(columns={'TagURL':'URL'}))
    count = sum(scrobbles['PlayCount'])
    if len(df) == 0:
        df['Percent'] = 1
    else:
        df['Percent'] = df.apply(lambda r: r.Score / count, axis=1)
    if len(df) == 0:
        df['PercentPretty'] = '100%'
    else:
        df['PercentPretty'] = df.apply(lambda r: str(round(r.Percent * 100)) + '%', axis=1)
    return df[df.index.get_level_values(0) != 'seen live']