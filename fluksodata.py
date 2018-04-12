import os
import tmpo
from tqdm import tqdm


def sync_and_get(group, start, end, resolution):
    session = tmpo.Session()

    for _, row in group.iterrows():
        session.add(sid=row.SensorId, token=row.Token)
    session.sync(*group.SensorId.values)

    data = session.get_data(
        sids=group.SensorId.values,
        head=start, tail=end,
        resolution=resolution,
        tz='Europe/Brussels',
        diff=True
    )

    return data


def export_data(sensors_tokens, grouper=None, start=None, end=None, resolution=None, data_format='multicolumn',
                path=None, file_format='csv'):

    if grouper is not None:
        grouped = sensors_tokens.groupby(grouper)
    else:
        grouped = ('data', sensors_tokens)

    for group_name, group in tqdm(grouped):
        data = sync_and_get(
            group=group,
            start=start,
            end=end,
            resolution=resolution
        )

        if data_format == 'normalized':
            data = data.unstack().reset_index()
            data.columns = ['SensorId', 'Timestamp', 'Value']

        friendly_name = str(group_name).strip("'()'").replace("', '", '_')
        if not path:
            path = ''
        out_path = os.path.join(path, friendly_name)

        if file_format == 'csv':
            data.to_csv('{}.csv'.format(out_path))
        elif file_format == 'pkl':
            data.to_pickle('{}.pkl'.format(out_path))

        print('Wrote {}'.format(out_path))