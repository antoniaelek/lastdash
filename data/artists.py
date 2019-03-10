import pandas as pd


def get_artists(filename='csv/artists.csv'):
    artists = (pd.read_csv(filename, names=['Count', 'Name', 'URL', 'ImageURL'], header=None, sep='\t')
               .dropna(subset=['Name'])
               .sort_values(by=['Count'], ascending=False)
               .set_index('Name'))
    count = sum(artists['Count'])
    artists['Percent'] = artists.apply(lambda r: r.Count / count, axis=1)
    artists['PercentPretty'] = artists.apply(lambda r: str(round(r.Percent, 2) * 100) + '%', axis=1)
    return artists
