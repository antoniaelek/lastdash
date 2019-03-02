import pandas as pd


def get_obsessions(scrobbles, palette, threshold=9):
    scrobbles['Cnt'] = 1
    obsessions = scrobbles[['Date', 'Artist', 'Track', 'URL', 'Cnt']].groupby(['Date', 'Artist', 'Track', 'URL'])[
        'Cnt'].sum()
    obsessions = obsessions.to_frame().reset_index()
    obsessions = obsessions.sort_values(by=['Date', 'Cnt'], inplace=False, ascending=False)
    obsessions = obsessions.groupby(['Date']).first()
    obsessions['Color'] = obsessions.apply(lambda r: palette[abs(hash(r.Artist) % len(palette))], axis=1)

    grouped = obsessions.groupby(['Artist', 'Track']).first()
    obsessions_array = grouped[grouped['Cnt'] > threshold]['URL'].values

    return obsessions[obsessions['URL'].isin(obsessions_array)]


def get_scrobbles(filename="csv/scrobbles.csv", header=None, sep='\t'):
    fields = ['Timestamp', 'Track', 'Artist', 'Album', 'URL']
    return _get_entries(filename, fields, header, sep)


def get_loved_tracks(filename="csv/loved-tracks.csv", header=None, sep='\t'):
    fields = ['Timestamp', 'Track', 'Artist', 'URL']
    return _get_entries(filename, fields, header, sep)


def _get_entries(filename, fields, header, sep):
    entries = pd.read_csv(filename, names=fields, header=header, sep=sep)
    entries['Timestamp'] = pd.to_datetime(entries['Timestamp'].str[:20], format='%Y-%m-%d %H:%M:%S')
    entries = entries[entries['Timestamp'] > "1970"]
    entries.sort_values(by=['Timestamp'], inplace=True, ascending=True)
    entries.dropna(subset=['Artist'], inplace=True)

    entries['Date'] = entries.apply(lambda r: r.Timestamp.date(), axis=1)
    entries['MonthByYearStr'] = entries.apply(lambda r: str(r.Timestamp.year) + '-' + (str(r.Timestamp.month) if r.Timestamp.month > 9 else '0' + str(r.Timestamp.month)), axis=1)
    entries['MonthByYear'] = entries.apply(lambda r: int(r.MonthByYearStr[:4]) + int(r.MonthByYearStr[-2:]) / 13 , axis=1)
    entries['Year'] = entries.apply(lambda r: r.Timestamp.year, axis=1)
    entries['Month'] = entries.apply(lambda r: r.Timestamp.month, axis=1)

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    entries['Weekday'] = entries.apply(lambda r: weekdays[r.Timestamp.weekday()], axis=1)
    entries['WeekdayNo'] = entries.apply(lambda r: r.Timestamp.weekday(), axis=1)
    entries['IsWeekend'] = entries.apply(lambda r: int(r.Timestamp.weekday()) > 4, axis=1)

    entries['Time'] = entries.apply(lambda r: r.Timestamp.time(), axis=1)
    entries['Hour'] = entries.apply(lambda r: r.Timestamp.time().hour, axis=1)
    return entries