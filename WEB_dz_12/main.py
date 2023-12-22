import uvicorn
from fastapi import FastAPI

from src.routes import route_contacts, route_auth

app = FastAPI()

app.include_router(route_contacts.router, prefix='/api', tags=['contacts'])
app.include_router(route_auth.router, prefix='/api', tags=['authentification'])


@app.get("/")
def read_root():
    return {"message": "Hello World"}


#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
