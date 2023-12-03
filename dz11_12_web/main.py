from fastapi import FastAPI
from .authentication import authenticate_user, create_access_token, UserCreate
from .contacts import app as contacts_app

app = FastAPI()

# Include other routers
app.include_router(contacts_app)


@app.post("/token", response_model=dict)
async def login_for_access_token(user: UserCreate):
    db_user = authenticate_user(user.email, user.password)
    if db_user:
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}
