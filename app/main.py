from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from time import time_ns

import pandas as pd
import uvicorn

from data.other import fields
from data.other import response_forms
from common_functions.response_formatter import response_formatter

from fields.field_types import AVAILABLE_FIELDS
from fields.field_interpreter import FieldInterpreter

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

fi = FieldInterpreter(AVAILABLE_FIELDS)

@app.get("/")
def read_root():
    return {"Welcome to": "data generator."}


@app.post("/generate_dataset")
async def get_body(request: Request):

    request_json = await request.json()
    request_dict = dict(request_json)
    fields_data = request_dict.get("fields")
    general_data = request_dict.get('general')

    # compare default data to requested data
    field_params = fields.request_checker(fields_data,
                                          fields.AVAILABLE_FIELDS)

    required_cols = fields.check_dependencies(fields_data)
    
    
    requested_cols = {}
    for key in fields_data.keys():
        custom_col_name = fields_data[key].get("custom_col_name") if fields_data[key].get(
            "custom_col_name") is not None else key
        blanck_chance = fields_data[key].get(
            "blanck_chance") if fields_data[key].get("blanck_chance") else 0
        requested_cols[key] = {"custom_col_name": custom_col_name,
                               "blanck_chance": blanck_chance}
        
    rows = general_data.get("rows", 1)
    for i in range(2):
        if i%2 == 0:
            required_cols = set(requested_cols.keys())
        start_time = time_ns()
        response = pd.DataFrame()
        
        if "id" in requested_cols:
        
            response["id"] = [i for i in range(rows)]
        
        people_res = People.generate_dataset(rows=rows,
                                            gender=field_params["gender"],
                                            age=field_params["age"],
                                            first_name=field_params["first_name"],
                                            last_name=field_params["last_name"],
                                            required_cols=required_cols)
        response = pd.concat([people_res, response],axis=1)
        areas_res = Areas.generate_dataset(rows=rows,
                                        base_df=response,
                                        voivodeship=field_params["voivodeship"],
                                        postcode=field_params["postcode"],
                                        required_cols=required_cols)

        response = pd.concat([response, areas_res],axis=1)
        athletes_res = Athletes.generate_dataset(rows=rows,
                                                base_df=response,
                                                sportstatus=field_params["sportstatus"],
                                                sportdiscipline=field_params["sportdiscipline"],
                                                required_cols=required_cols)

        print(field_params["sportstatus"])

        response = pd.concat([response, athletes_res],axis=1)
        education_res = Education.generate_dataset(rows=rows,
                                                base_df=response,
                                                languages=field_params["languages"],
                                                edu_level=field_params["edu_level"],
                                                required_cols=required_cols)

        response = pd.concat([response, education_res],axis=1)
        
        response_format = str(general_data.get("response_format"))
        print(f"generate dataset time in ns with {['all cols', 'only required cols'][i]}: ",(time_ns()-start_time)/1000**3)
    
    return response_formatter(response, requested_cols, field_params.get("id"), response_format)


@app.get("/available_fields")
async def available_fields():
    """Return available `fields` with possible modifications
    mainly customized to API GUI.
    """
    return {
        "fields": fields.AVAILABLE_FIELDS,
        "general": response_forms.RESPONSE_FORMS
    }

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
