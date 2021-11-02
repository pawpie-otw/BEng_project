from typing import Optional
from fastapi import FastAPI, Query
from person import Person

import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}", disable_extra_fields=True)
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/person/")
def person():
    return {"sex": Person.draw_sex()}


@app.get("/query")
async def query(q=Query(None)):
    return {"q": int(q)}

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
