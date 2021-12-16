from typing import Optional
from fastapi import FastAPI, Query
from people import People
<<<<<<< HEAD
import pandas as pd
=======
from athletes import Athletes

>>>>>>> sports
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


<<<<<<< HEAD
@app.get("/people/{n}")
async def person(n: int = Query(1, description="number of returned records, >=1", ge=1),
                 age_low_lim: int = Query(None,
                                          description="lowest limit of drawing age, have to be lower or equal to upper limit", ge=0, le=100),
                 age_up_lim: int = Query(None,
                                         description="upper limit of drawing age, have to be upper or equal to lower limit", ge=0, le=100),
                 only_males: bool = Query(False),
                 only_females: bool = Query(False),
                 number_of_fnames: int = Query(1,
                                               description="number of first names", ge=1, le=3),
                 unregular_number_of_names: bool = Query(
        False, description="if number of names is >1, then you can set this param to true and some of people will have less then number_of_fnames names"),
        double_surnames: bool = Query(
            False, description="If true, there is a chance to draw double surname in records"),
        orient: str = Query('split',
                            description="orient of returned json (‘split’, ‘records’, ‘index’, ‘table’), for more look at pandas to_json docs")):
    res = People.generate_dataset(n=n,
                                  age_low_lim=age_low_lim,
                                  age_up_lim=age_up_lim,
                                  only_males=only_males,
                                  only_females=only_females)
    #

    return res.to_json(orient=orient)
=======
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/person/")
def person():
    return {"sex": People.generate_dataset()}

@app.get("/athlete/")
def athlete():
    return {"0": Athletes.generate_dataset()}

@app.get("/query")
async def query(q=Query(None)):
    return {"q": int(q)}
>>>>>>> sports

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
