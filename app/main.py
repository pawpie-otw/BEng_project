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
    return {"Hello": "World"}


# @app.get("/people/{n}")
# async def person(n: int = Query(1, description="number of returned records, >=1", ge=1),
#                  age_low_lim: int = Query(None,
#                                           description="lowest limit of drawing age, have to be lower or equal to upper limit", ge=0, le=100),
#                  age_up_lim: int = Query(None,
#                                          description="upper limit of drawing age, have to be upper or equal to lower limit", ge=0, le=100),
#                  only_males: bool = Query(False),
#                  only_females: bool = Query(False),
#                  number_of_fnames: int = Query(1,
#                                                description="number of first names", ge=1, le=3),
#                  unregular_number_of_fnames: bool = Query(
#         False, description="if number of names is >1, then you can set this param to true and some of people will have less then number_of_fnames names"),
#         double_surnames: bool = Query(
#             False, description="If true, there is a chance to draw double surname in records"),
#         indexed_cols: bool = Query(True),
#         orient: str = Query('typical_json_form',
#                             description="orient of returned json (‘split’, ‘records’, ‘index’, ‘table’, 'typical_json_form'), for more look at pandas to_json docs")):

#     people_res = People.generate_dataset(n=n,
#                                          age_low_lim=age_low_lim,
#                                          age_up_lim=age_up_lim,
#                                          only_males=only_males,
#                                          only_females=only_females,
#                                          number_of_fnames=number_of_fnames,
#                                          unregular_number_of_fnames=unregular_number_of_fnames)
    
    
    
#     # athlets_res = Athletes.generate_dataset(people_res)  # return series of sport



#     if orient == "typical_json_form":
#         return json_form(people_res.merge(areas_res, left_index=True, right_index=True))

#     return people_res.to_json(orient=orient, index=indexed_cols, force_ascii=False)


@app.post("/generate_dataset")
async def get_body(request: Request):
    
    request_json = await request.json()
    request_dict = dict(request_json)
    rows = request_dict.get('rows')
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
    
    
    response_format = str(request_dict.get("response_format"))
    
    return response_formatter(pd.concat([people_res, areas_res, athletes_res],axis=1),
                              response_format)

@app.get("/available_fields")
async def available_fields():
    """Return available `fields` with possible modifications
    mainly customized to API GUI.
    """
    return fields.available_fields

@app.get("/available_response_forms")
async def available_response_forms():
    return {
            "fields": response_forms.response_forms,
            "return_fields": response_forms.return_params
            }

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
    
