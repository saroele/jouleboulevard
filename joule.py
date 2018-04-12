import pandas as pd
meta = pd.read_csv('jouleboulevard_metadata.csv')
meta.index = meta['SensorId']

def filter_meta(**kwargs):

    res = meta.copy()
    for k,v in kwargs.items():
        res = res[res.loc[:,k] == v]

    return res