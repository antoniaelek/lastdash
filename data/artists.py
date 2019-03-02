import pandas as pd


def get_artists(filename='csv/artists.csv'):
    artists = pd.read_csv(filename, names=['Count', 'Name', 'URL'], header=None, sep='\t')
    artists.sort_values(by=['Count'], inplace=True, ascending=False)
    artists.dropna(subset=['Name'], inplace=True)
    return artists
