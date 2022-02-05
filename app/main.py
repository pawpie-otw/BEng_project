import time
from typing import Sequence, Any, Union
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import pandas as pd
import uvicorn

from common_functions.extra_funcs import make_cols_unique

from fields.dependencies import DEPENDENCIES
from fields.field_types import AVAILABLE_FIELDS
from fields.field_interpreter import FieldInterpreter
from fields.example_request import EXAMPLE_BODY

from response.response_interpreter import ResponseInterpreter
from response.response_types import RESPONSE_PARAMS, RESPONSES_FOR_CONVERTER

from people import People
from areas import Areas
from athletes import Athletes
from education import Education

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fi = FieldInterpreter(AVAILABLE_FIELDS, DEPENDENCIES)
ri = ResponseInterpreter(RESPONSES_FOR_CONVERTER)


@app.get("/")
def read_root():
    return {"Welcome to": "data generator."}


@app.post("/generate_dataset")
async def generate_dataset(request: Request) -> Union[str, 'JSON']:
    """This is key method of `Generator danych z API` which returns synthetic generated data
    based on statistic from Poland. Let's check out our server dedicated web page for more
    user-friendly experience.
    Example of the accepted request body/data looks like this one:\n


```
    {
    "id": {
        "custom_col_name": null
    },
    "gender": {
        "custom_col_name": null,
        "equal_weight": false,
        "blank_chance": 0
    },
    "age": {
        "custom_col_name": null,
        "low_lim": 0,
        "up_lim": 100,
        "equal_weight": false,
        "blank_chance": 0
    },
    "first_name": {
        "custom_col_name": null,
        "double_name_chance": 0,
        "equal_weight": false,
        "unfit_to_gen": false,
        "blank_chance": 0
    },
    "last_name": {
        "custom_col_name": null,
        "double_name_chance": 0,
        "equal_weight": false,
        "unfit_to_gen": false,
        "blank_chance": 0
    },
    "voivodeship": {
        "custom_col_name": null,
        "equal_weight": false,
        "blank_chance": 0
    },
    "postcode": {
        "custom_col_name": null,
        "independently": false,
        "blank_chance": 0
    },
    "sportstatus": {
        "custom_col_name": null,
        "independently": false,
        "without_null": false,
        "equal_weight": false,
        "blank_chance": 0
    },
    "sportdiscipline": {
        "custom_col_name": null,
        "without_null": false,
        "equal_weight": false,
        "blank_chance": 0
    },
    "languages": {
        "custom_col_name": null,
        "equal_weight": false,
        "without_null": false,
        "blank_chance": 0
    },
    "edu_level": {
        "custom_col_name": null,
        "equal_weight": false,
        "without_null": false,
        "ignore_age": false,
        "blank_chance": 0
        } 
    }
    ```

    It contains all available field with all options set to default value.

    Returns:
        It returns string in csv, LaTeX/HTML table or just json.
    """
    request_json = await request.json()
    request_dict = dict(request_json)
    fields_data = request_dict.get("fields")
    general_data = request_dict.get("general")

    if (len(requested_cols := fields_data.keys()) == 10 and "id" not in requested_cols) or len(requested_cols) == 11:
        fixed_request = fi.fix_request(fields_data)
    cols_to_refill = fi.check_requested_cols_for_dependencies(fixed_request)
    refilled = fi.refill_multiple_fields(cols_to_refill)
    refilled.update(fixed_request)
    # compare default data to requested data

    required_cols = set(refilled.keys())

    rows = general_data.get("rows", 1)
    response_form = general_data.get("response_format", "json")

    response = pd.DataFrame()

    if "id" in required_cols:
        response["id"] = range(rows)

    start = time.time()

    people_res = People.generate_dataset(rows=rows,
                                         gender=refilled.get("gender"),
                                         age=refilled.get("age"),
                                         first_name=refilled.get(
                                             "first_name"),
                                         last_name=refilled.get(
                                             "last_name"),
                                         required_cols=required_cols)
    response = pd.concat([people_res, response], axis=1)
    areas_res = Areas.generate_dataset(rows=rows,
                                       base_df=response,
                                       voivodeship=refilled.get(
                                           "voivodeship"),
                                       postcode=refilled.get("postcode"),
                                       required_cols=required_cols)

    response = pd.concat([response, areas_res], axis=1)
    athletes_res = Athletes.generate_dataset(rows=rows,
                                             base_df=response,
                                             sportstatus=refilled.get(
                                                 "sportstatus"),
                                             sportdiscipline=refilled.get(
                                                 "sportdiscipline"),
                                             required_cols=required_cols)

    response = pd.concat([response, athletes_res], axis=1)
    education_res = Education.generate_dataset(rows=rows,
                                               base_df=response,
                                               languages=refilled.get(
                                                   "languages"),
                                               edu_level=refilled.get(
                                                   "edu_level"),
                                               required_cols=required_cols)

    gen_exe = time.time()

    response = pd.concat([response, education_res], axis=1)

    cutted_df = response[requested_cols]

    unique_names = make_cols_unique(options["custom_col_name"]
                                    for options in fixed_request.values())

    cutted_df.columns = [ucn if ucn is not None
                         else col_name
                         for col_name, ucn in zip(fixed_request, unique_names)]

    x = ri.convert_df(cutted_df, response_form)

    data_converting = time.time()

    print(f"ilosc danych wygenerowanych: {rows}x{len(required_cols)}")
    print(f"ilosc danych zwroconych: {rows}x{len(required_cols)}")
    print(f"czas generowania: {gen_exe - start}")
    print(f"formating time {data_converting - gen_exe}")
    return x


@app.get("/available_fields")
async def available_fields():
    """Return available `fields` with possible modifications
    mainly customized to API GUI.
    """
    return {
        "fields": AVAILABLE_FIELDS,
        "general": RESPONSE_PARAMS
    }


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
