import io
from fastapi.responses import StreamingResponse
from common_functions import loggers


class ResponseInterpreter:
    
    @staticmethod
    @loggers.timeit_and_log("./logs/response.logs")
    def convert_df(data, method_name)->StreamingResponse :
        
        if method_name == "json":
            return data.to_json(orient="records")
        
        stream = io.StringIO()
        {"to_csv": data.to_csv(stream, index=False),
        "to_html": data.to_html(stream, index=False),
        "to_latex": data.to_latex(stream, index=False)}[method_name]

        file_type = method_name.split("_")[1]
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type=f"text/{file_type}")

        response.headers["Content-Disposition"] = f"attachment; filename=export.{file_type}"

        return response