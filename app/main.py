from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware 

import pandas as pd
import uvicorn 

from data.other import fields
from data.other import response_forms
from common_functions.response_formatter import response_formatter

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
                                          fields.available_fields)
    
    requested_cols = {}
    
    for key in fields_data.keys():
        custom_col_name =fields_data[key].get("custom_col_name") if fields_data[key].get("custom_col_name") is not None else key
        blanck_chance = fields_data[key].get("blanck_chance") if fields_data[key].get("blanck_chance") else 0
        requested_cols[key]={"custom_col_name":custom_col_name,
                             "blanck_chance":blanck_chance}
    
    
    rows = general_data.get("rows") if general_data.get("rows") is not None else 1
    
    people_res = People.generate_dataset(rows = rows,
                                         gender = field_params["gender"],
                                         age = field_params["age"],
                                         first_name = field_params["first_name"],
                                         last_name = field_params["last_name"])
    
    areas_res = Areas.generate_dataset(rows = rows,
                                        base_df = people_res,
                                        voivodeship=field_params["voivodeship"],
                                        postcode=field_params["postcode"])
    
    athletes_res = Athletes.generate_dataset(rows = rows
                                             ,base_df=pd.concat([people_res['age'], areas_res['voivodeship']],axis=1)
                                             ,sportstatus=field_params["sportstatus"]
                                             ,sportdiscipline=field_params["sportdiscipline"]
                                             )
    
    education_res = Education.generate_dataset(rows = rows
                                               ,base_df = people_res
                                               ,languages = field_params["languages"]
                                               ,education = field_params["education"]
                                               )
    
    response_format = str(general_data.get("response_format"))
    return response_formatter(pd.concat([people_res, areas_res, athletes_res, education_res],axis=1),
                              requested_cols,
                              response_format)

@app.get("/available_fields")
async def available_fields():
    """Return available `fields` with possible modifications
    mainly customized to API GUI.
    """
    return {
            "fields": fields.available_fields,
            "general": response_forms.response_forms
            }

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
    
