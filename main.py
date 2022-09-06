# main.py

from fastapi import FastAPI
from routers import user, bundles, options, orders, shoppes

app = FastAPI()

# Common
app.include_router(user.router)

# Mum Shoppes
app.include_router(shoppes.router)
app.include_router(bundles.router)
app.include_router(options.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
