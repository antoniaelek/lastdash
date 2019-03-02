import pandas as pd


def get_tags(filename='csv/tags.csv'):
    tags = pd.read_csv(filename, names=['Count', 'Name', 'URL'], header=None, sep='\t')
    tags.sort_values(by=['Count'], inplace=True, ascending=False)
    tags.dropna(subset=['Name'], inplace=True)
    count = sum(tags['Count'])
    tags['Percent'] = tags.apply(lambda r: r.Count/count, axis=1)
    tags['PercentPretty'] = tags.apply(lambda r: str(round(r.Percent,2)*100) + '%', axis=1)
    return tags
