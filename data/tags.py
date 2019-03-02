import pandas as pd


def get_tags(filename='csv/tags.csv'):
    tags = pd.read_csv(filename, names=['Count', 'Name', 'URL'], header=None, sep='\t')
    tags.sort_values(by=['Count'], inplace=True, ascending=False)
    tags.dropna(subset=['Name'], inplace=True)
    return tags
