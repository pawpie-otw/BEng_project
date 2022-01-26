import io
import pandas as pd

from typing import Tuple, Dict, Any

from fastapi.responses import StreamingResponse


class ResponseInterpreter:
    def __init__(self, convert_form: dict = {}):
        self.convert_form = convert_form

    def convert_df(self, data, method_name):
        method = self.convert_form[method_name]

        if method["method_group"] == "pandas":
            return self.pandas_methods(data, method_name)

        if method["method_group"] == "custom":
            return self.json_form(data)

    def pandas_methods(self, data, method_name):
        stream = io.StringIO()

        if method_name == "to_csv":
            data.to_csv(stream, index=False)
        elif method_name == "to_html":
            data.to_html(stream, index=False)
        elif method_name == "to_latex":
            data.to_latex(stream, index=False)
        else:
            return self.json_form(data)

        file_type = method_name.split("_")[1]
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type=f"text/{file_type}")

        response.headers["Content-Disposition"] = f"attachment; filename=export.{file_type}"

        return response

    def json_form(self, df: pd.DataFrame) -> Tuple[Dict[str, Any]]:
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
        return tuple({col: self.pandas_to_def_mapper(df.iloc[i][col])
                      for col in cols}
                     for i in range(len(df.index)))

    @staticmethod
    def pandas_to_def_mapper(var):
        """This method map pandas dtype to typical python data types like str, int itd.
        """
        if var is None:
            return None
        elif isinstance(var, float):
            return float(var)
        elif isinstance(var, str):
            if var == "":
                return None
            return str(var)
        return int(var)
