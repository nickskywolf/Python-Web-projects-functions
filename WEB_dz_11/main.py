from fastapi import FastAPI

from src.routes import route_contacts

app = FastAPI()

app.include_router(route_contacts.router, prefix='/api', tags=['contacts'])


@app.get("/")
def read_root():
    return {"message": "Hello World"}
