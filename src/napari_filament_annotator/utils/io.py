import pandas as pd


def annotation_to_pandas(data: list, col_name='id') -> pd.DataFrame:
    """
    Convert list of path to a pandas table with coordinates.

    Parameters
    ----------
    data : list
        List of paths, each of which is a list of coordinates.

    Returns
    -------
    pd.DataFrame:
        pandas DataFrame with coordinates
    """

    df = pd.DataFrame()
    if len(data) > 0:
        columns = ['t', 'z', 'y', 'x']
        columns = columns[-data[0].shape[1]:]
        for i, d in enumerate(data):
            cur_df = pd.DataFrame(d, columns=columns)
            cur_df[col_name] = i
            df = pd.concat([df, cur_df], ignore_index=True)
    return df


def pandas_to_annotations(df: pd.DataFrame, col_name='id') -> list:
    columns = ['z', 'y', 'x']
    data = []
    labels = []
    if len(df) > 0:
        for s in df[col_name].unique():
            d = df[df[col_name] == s][columns].values
            data.append(d)
            labels.append(s)
    return data, labels
