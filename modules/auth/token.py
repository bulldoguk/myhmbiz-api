from fastapi import Header, HTTPException, status
import requests


async def token_required(x_token: str = Header()):
    if not x_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No token provided')

    try:
        encoded = x_token.split()[1]
        uri = 'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=' + encoded
        validate = requests.get(uri).json()
        if int(validate.get('expires_in')) > 0 and validate.get('email_verified') == 'true':
            #TODO: This is where we need to create our own JWT access token
            return True
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')


class AccessToken:
    pass
