import pandas as pd


def get_artists(filename='csv/artists.csv'):
    artists = pd.read_csv(filename, names=['Count', 'Name', 'URL'], header=None, sep='\t')
    artists.sort_values(by=['Count'], inplace=True, ascending=False)
    artists.dropna(subset=['Name'], inplace=True)
    count = sum(artists['Count'])
    artists['Percent'] = artists.apply(lambda r: r.Count/count, axis=1)
    artists['PercentPretty'] =artists.apply(lambda r: str(round(r.Percent,2)*100) + '%', axis=1)
    return artists
