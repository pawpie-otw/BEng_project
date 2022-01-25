
import pandas as pd
from fastapi.responses import StreamingResponse
import io
class ResponseInterpreter:
    def __init__(self):
        pass
    
    def csv_stream(self, df:pd.DataFrame):
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        filetype = "csv"
        response = StreamingResponse(iter([stream.getvalue()]), media_type=f"text/{filetype}")

        response.headers["Content-Disposition"] = f"attachment; filename=export.{filetype}"

        return response
    