# tests/dummy_app.py
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/api/home", status_code=status.HTTP_200_OK)
async def home():
    return {"ok": True}


@app.post("/login", status_code=status.HTTP_200_OK)
async def login():
    return {"token": "xyz"}


@app.get("/register", status_code=status.HTTP_200_OK)
async def register():
    return {"msg": "welcome"}
