from typing import Dict, Tuple, Any

import pandas as pd #type: ignore


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
    if var is None:
        return None
    elif isinstance(var, str):
        return str(var)
    return int(var)


def response_formatter(df:pd.DataFrame,
                  columns_names: Dict[str,str],
                  requested_format: str = "json",
                  *args, **kwargs)->Any:
    
    """Return pd.DataFrame in `type_name` form.

    Args:
        format_type (str): the format in which you will receive the data.
        available formats:
            - "typical_json",\n
            - "html table",  \n
            - "csv",         \n
            - "markdown".    \n

    Returns:
        Any: return pd.DataFrame converted into one of available format.
    """
    
    response_df = df[columns_names.keys()]
    response_df.columns = [columns_names[key]
                           for key in columns_names]
    
    available_response_formats = {
        "json": json_form,
        "html table":pd.DataFrame.to_html,
        "csv":pd.DataFrame.to_csv,
        "markdown": pd.DataFrame.to_markdown
        }
    
    for format, method in available_response_formats.items():
        if format == requested_format:
            return method(response_df, *args, **kwargs)