from typing import Dict, Tuple, Any
import pandas as pd


def json_form(df: pd.DataFrame, id_column:str="id") -> Tuple[Dict[str, Any]]:
    """Convert pandas df to 
    >>> [{field_name -> value},
    ... {field_name -> value} ...] 
    format, better to convert to json.

    Args:
        df (pd.DataFrame): DF to convert.
        id_column (str): if not None, then add to every object id with id_column name, else no.

    Returns:
        Tuple[Dict[str, Any]]: Returned data.
    """
    if id_column:
        df.insert(loc=0, column=id_column, value=df.index)
    cols = df.columns
    return tuple({col: to_def_type(df.iloc[i][col])
            for col in cols}
            for i in range(len(df.index)))

def to_def_type(var):
    if isinstance(var, str):
        return str(var)
    return int(var)