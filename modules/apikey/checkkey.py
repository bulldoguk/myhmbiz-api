from fastapi import Header, HTTPException
from decouple import config

async def verify_key(x_key: str = Header()):
    if x_key != config('APIKEY'):
        raise HTTPException(status_code=403, detail='Unauthorized access')