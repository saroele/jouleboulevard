import pandas as pd
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

