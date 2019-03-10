import pandas as pd


def get_obsessions(scrobbles, threshold=9):
    scrobbles['Cnt'] = 1
    period_start = scrobbles['Date'].min()
    period_end = scrobbles['Date'].max()
    period = pd.date_range(start=period_start, end=period_end)

    cnt_daily = scrobbles[['Date', 'Artist', 'Track', 'URL', 'Cnt']].groupby(['Date', 'Artist', 'Track', 'URL'])['Cnt'].sum()
    cnt_daily = cnt_daily.to_frame().reset_index()

    out_df = pd.DataFrame()
    urls = scrobbles['URL'].unique()
    for url in urls:
        curr_track_cnt = cnt_daily[cnt_daily['URL'] == url]
        artist = curr_track_cnt['Artist'].iloc[0]
        track = curr_track_cnt['Track'].iloc[0]
        curr_track_cnt = curr_track_cnt[['Date', 'Cnt']].set_index('Date')

        for date in period:
            if date not in curr_track_cnt.index:
                curr_track_cnt.loc[date] = 0

        curr_track_cnt = curr_track_cnt.sort_values(by=['Date'], inplace=False, ascending=True)
        curr_track_cnt_windows = curr_track_cnt.rolling(3, min_periods=1).sum()
        curr_track_cnt_windows = curr_track_cnt_windows.rename(index=str, columns={"Cnt": "WindowCnt"})

        final = curr_track_cnt.join(curr_track_cnt_windows)
        final['Artist'] = artist
        final['Track'] = track
        final['URL'] = url

        out_df = pd.concat([out_df, final])

    out_df = out_df.sort_values(by=['URL', 'Date'], inplace=False, ascending=True)
    return out_df#[out_df['Cnt'] > threshold]


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