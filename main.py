# main.py

from fastapi import FastAPI, Depends
from routers import user, bundles, options, orders, shoppes
from modules.apikey import checkkey
from decouple import config
from fastapi.middleware.cors import CORSMiddleware

if not config('DEVELOPMENT'):
    app = FastAPI(dependencies=[Depends(checkkey.verify_key)])
else:
    app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Common
app.include_router(user.router)

# Mum Shoppesß
app.include_router(shoppes.router)
app.include_router(bundles.router)
app.include_router(options.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
