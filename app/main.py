from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from time import time_ns

import pandas as pd
import uvicorn

from data.other import response_forms
from common_functions.response_formatter import response_formatter

from fields.dependencies import DEPENDENCIES
from fields.field_types import AVAILABLE_FIELDS
from fields.field_interpreter import FieldInterpreter

from response.response_interpreter import ResponseInterpreter

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
ri = ResponseInterpreter()
@app.get("/")
def read_root():
    return {"Welcome to": "data generator."}


@app.post("/generate_dataset")
async def get_body(request: Request):

    request_json = await request.json()
    request_dict = dict(request_json)
    fields_data = request_dict.get("fields")
    general_data = request_dict.get('general')

    fixed_request = fi.fix_request(fields_data)
    cols_to_refill =  fi.check_requested_cols_for_dependencies(fixed_request)
    refilled = fi.refill_multiple_fields(cols_to_refill)
    refilled.update(fixed_request)
    # compare default data to requested data

    required_cols = set(refilled.keys())
        
    rows = general_data.get("rows", 1)
    
    print(required_cols)
    for i in range(2):
        response = pd.DataFrame()
        
        people_res = People.generate_dataset(rows=rows,
                                            gender=refilled.get("gender"),
                                            age=refilled.get("age"),
                                            first_name=refilled.get("first_name"),
                                            last_name=refilled.get("last_name"),
                                            required_cols=required_cols)
        response = pd.concat([people_res, response],axis=1)
        areas_res = Areas.generate_dataset(rows=rows,
                                        base_df=response,
                                        voivodeship=refilled.get("voivodeship"),
                                        postcode=refilled.get("postcode"),
                                        required_cols=required_cols)

        response = pd.concat([response, areas_res],axis=1)
        athletes_res = Athletes.generate_dataset(rows=rows,
                                                base_df=response,
                                                sportstatus=refilled.get("sportstatus"),
                                                sportdiscipline=refilled.get("sportdiscipline"),
                                                required_cols=required_cols)

        response = pd.concat([response, athletes_res],axis=1)
        education_res = Education.generate_dataset(rows=rows,
                                                base_df=response,
                                                languages=refilled.get("languages"),
                                                edu_level=refilled.get("edu_level"),
                                                required_cols=required_cols)

        response = pd.concat([response, education_res],axis=1)
        
    
    return ri.csv_stream(response)


@app.get("/available_fields")
async def available_fields():
    """Return available `fields` with possible modifications
    mainly customized to API GUI.
    """
    return {
        "fields": AVAILABLE_FIELDS,
        "general": response_forms.RESPONSE_FORMS
    }

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
