from fastapi import FastAPI, Request # type: ignore

from athletes import Athletes
import pandas as pd # type: ignore
import uvicorn # type: ignore

from common_functions.response_formatter import response_formatter
from people import People
from areas import Areas
from data.athletes.sports_data import Data
from data.other import fields
from data.other import response_forms

app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome to": "data generator."}

@app.post("/generate_dataset")
async def get_body(request: Request):
    
    request_json = await request.json()
    request_dict = dict(request_json)
    general_data = request_dict.get('general')
    rows = general_data.get("rows") if general_data.get("rows") is not None else 1
    people_res = People.generate_dataset(rows = rows,
                                         gender = request_dict.get("gender"),
                                         age = request_dict.get("age"),
                                         first_name = request_dict.get("first_name"),
                                         last_name = request_dict.get("last_name"))
    
    areas_res = Areas.generate_dataset(rows = rows,
                                        base_df = pd.DataFrame(people_res),
                                        voivodeship=request_dict.get("voivodeship"),
                                        postcode=request_dict.get("postcode"))
    
    athletes_res = Athletes.generate_dataset(rows = rows,
                                             base_df=pd.concat([people_res['age'], areas_res['voivodeship']],axis=1),
                                             sportstatus=request_dict.get("sportstatus"),
                                             sportdyscipline=request_dict.get("sportdyscypline"))
    
    
    response_format = str(general_data.get("response_format"))
    
    return response_formatter(pd.concat([people_res, areas_res, athletes_res],axis=1),
                              response_format)

@app.get("/available_fields")
async def available_fields():
    """Return available `fields` with possible modifications
    mainly customized to API GUI.
    """
    return {
            "fields": response_forms.response_forms,
            "general": response_forms.return_params
            }
    

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
    
