import uvicorn
from fastapi import FastAPI
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from src.routes import route_contacts, route_auth, route_users

app = FastAPI()

app.include_router(route_contacts.router, prefix='/api', tags=['contacts'])
app.include_router(route_auth.router, prefix='/api', tags=['authentification'])
app.include_router(route_users.router, prefix='/api')

origins = [
    "http://localhost:3000"
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app,
    such as database connections or external services.
    :return: A list of functions to run after the server starts

    :return: A list of functions to be executed after the server starts
    :doc-author: Trelent
    """
    """    
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app,
    such as database connections or external services.
    :return: A list of functions to run after the server starts
    
    :return: A list of functions to be executed after the server starts
    :doc-author: Trelent
    """
    """    
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app,
    such as connecting to databases or initializing caches.
    
    :return: A list of functions to be executed
    :doc-author: Trelent
    """
    """    
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app,
    such as database connections or external services.
    
    :return: A list of functions to run after the server starts
    :doc-author: Trelent
    """
    red_limit = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(red_limit)


@app.get("/")
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;Hello World!&quot;.

    :return: A dictionary
    :doc-author: Trelent
    """
    """    
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;Hello World!&quot;.
    
    :return: A dictionary with a key &quot;message&quot; and the value &quot;hello world!&quot;
    :doc-author: Trelent
    """
    return {"message": "Hello World!"}





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
