import pandas as pd


def get_scrobbles_by_hour(scrobbles):
    return scrobbles[['Hour', 'PlayCount']].groupby('Hour').sum().reindex(list(range(0, 24)), fill_value=0)


def get_scrobbles(filename="csv/scrobbles.csv"):
    return _get_activity(filename=filename, fields=['Timestamp', 'Track', 'Artist', 'Album', 'URL', 'ImageURL'], header=None, sep='\t')


def _get_activity(filename, fields, header, sep):
    # Read csv
    entries = pd.read_csv(filename, names=fields, header=header, sep=sep)

    # Add Timestamp column
    entries['Timestamp'] = pd.to_datetime(entries['Timestamp'].str[:20], format='%Y-%m-%d %H:%M:%S')
    entries = entries[entries['Timestamp'] > "1970"]
    entries.sort_values(by=['Timestamp'], inplace=True, ascending=True)
    entries.dropna(subset=['Artist'], inplace=True)

    # Add Date columns
    entries['Date'] = entries.apply(lambda r: r.Timestamp.date(), axis=1)
    entries['Year'] = entries.apply(lambda r: r.Timestamp.year, axis=1)
    entries['Month'] = entries.apply(lambda r: r.Timestamp.month, axis=1)
    entries['YearMonth'] = entries.apply(lambda r: str(r.Timestamp.year) + '-' + (
    str(r.Timestamp.month) if r.Timestamp.month > 9 else '0' + str(r.Timestamp.month)), axis=1)

    # Add Weekday columns
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    entries['Weekday'] = entries.apply(lambda r: weekdays[r.Timestamp.weekday()], axis=1)
    entries['WeekdayNo'] = entries.apply(lambda r: r.Timestamp.weekday(), axis=1)
    entries['IsWeekend'] = entries.apply(lambda r: int(r.Timestamp.weekday()) > 4, axis=1)
    entries['Time'] = entries.apply(lambda r: r.Timestamp.time(), axis=1)
    entries['Hour'] = entries.apply(lambda r: r.Timestamp.time().hour, axis=1)

    # PlayCount column
    entries['PlayCount'] = 1

    # Set index
    entries.set_index(['Date', 'Artist', 'Track'], inplace=True)

    return entries
