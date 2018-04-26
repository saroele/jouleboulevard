import pandas as pd
import yaml
import datetime
from workalendar.europe import Belgium

meta = pd.read_csv('jouleboulevard_metadata.csv')
meta.index = meta['SensorId']

def filter_meta(**kwargs):

    res = meta.copy()
    for k,v in kwargs.items():
        res = res[res.loc[:,k] == v]

    return res

def remove_outliers(ts, min=0.05, max=0.95):
    """
    Parameters
    ----------
    df : pandas.Series
    min : float, default=0.05
        Remove outliers below this percentile
    max : float, default=0.95
        Remove outliers above this percentile

    Returns
    -------
    res : pandas.DataFrame or pandas.Series
    """

    ts_described = ts.describe(percentiles=[min, max])
    vmin = ts_described['{}%'.format(int(100*min))]
    vmax = ts_described['{}%'.format(int(100*max))]
    res=ts.copy()
    res[res<vmin] = pd.np.nan
    res[res>vmax] = pd.np.nan
    return res


def get_openinghours(ea_number, ts):
    df = pd.Series(data=False, index=ts.index)

    # Read YAML file
    with open("data/" + ea_number + ".yml", 'r') as stream:
        data_loaded = yaml.load(stream)
        for day in data_loaded:
            for key in day:
                hour_list = day[key]
                for hours in hour_list:
                    df = df | week_schedule(index=ts.index, on_days=[key], on_time=hours[0], off_time=hours[1],
                                            closed=[datetime.date(2018, 4, 25)])

    return df


def week_schedule(index, on_days, on_time=None, off_time=None, exclude_holidays=True, closed=None):
    cal = Belgium()

    if on_time is None:
        on_time = '9:00'
    if off_time is None:
        off_time = '17:00'

    if not isinstance(on_time, datetime.time):
        on_time = pd.to_datetime(on_time, format='%H:%M').time()
    if not isinstance(off_time, datetime.time):
        off_time = pd.to_datetime(off_time, format='%H:%M').time()

    times = (index.time >= on_time) & (index.time < off_time) & (index.weekday_name.isin(on_days))

    result = pd.Series(times, index=index)

    holidays = []
    years = list(range(index[0].year, index[-1].year + 1))
    for y in years:
        for d in cal.get_calendar_holidays(y):
            holidays.append(d[0])

    if exclude_holidays:
        result[result.index.map(lambda x: x.date() in holidays)] = False

    if closed is not None:
        if isinstance(closed[0], datetime.date):
            result[result.index.map(lambda x: x.date() in closed)] = False

    return result
