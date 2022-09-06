# main.py

from fastapi import FastAPI
from routers import user
from routers import bundles

app = FastAPI()

app.include_router(user.router)
app.include_router(bundles.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
