from typing import Dict, Tuple, Any
from common_functions import extra_funcs
from fastapi.responses import StreamingResponse
import io
import pandas as pd


def json_form(df: pd.DataFrame, id_column: str = "id") -> Tuple[Dict[str, Any]]:
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
    cols = df.columns
    return tuple({col: to_def_type(df.iloc[i][col])
                  for col in cols}
                 for i in range(len(df.index)))


def to_def_type(var):
    if var is None:
        return None
    if isinstance(var, float):
        return float(var)
    elif isinstance(var, str):
        if var == "":
            return None
        return str(var)
    return int(var)


def return_file(df:pd.DataFrame, filetype:str, dict_method:dict):
    """Convert df file to streamable form and return it.

    Args:
        df (pd.DataFrame): DataFrame to convert and return
        filetype (str): filetype (like `csv`) which is also key in `dict_method`.
        dict_method (dict): dict contains `filetype`:{`method_name`:method, }

    Returns:
        Ready to return file.
    """
    
    stream = io.StringIO()
    df.dict_metod_data[filetype](stream, index = False)
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type=f"text/{filetype}")
    
    response.headers["Content-Disposition"] = f"attachment; filename=export.{filetype}"
    
    return response



def response_formatter(df: pd.DataFrame,
                       columns_names: Dict[str, str],
                       field_id: dict,
                       requested_format: str = "json",
                       *args, **kwargs) -> Any:
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

    response_df = df[columns_names.keys()].fillna("")

    for key in columns_names:
        response_df[key] = extra_funcs.insert_value_randomly(response_df[key],
                                                             columns_names[key]["blanck_chance"])

    response_df.columns = [columns_names[key]["custom_col_name"]
                           for key in columns_names]

    available_response_formats = {
        "json": json_form,
        "html table": pd.DataFrame.to_html,
        "csv": pd.DataFrame.to_csv,
        "markdown": pd.DataFrame.to_markdown
    }

    for format, method in available_response_formats.items():
        if format == requested_format:
            if format == "json":
                return method(response_df, id_column=field_id.get("custom_col_name"))
            else:
                return method(response_df, *args, index=field_id.get("custom_col_name") is not None, **kwargs)