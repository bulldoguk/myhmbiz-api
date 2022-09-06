from flask import request, jsonify
import requests


def token_required(headers):
    token = None

    if headers:
        token = headers

    if not token:
        print(f'Kicking back token {token}')
        return jsonify({'result': False, 'message': 'a valid token is missing'})

    try:
        encoded = token.split()[1]
        uri = 'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=' + encoded
        # TODO: Need to find a way to cache this request to reduce hits on Google APIS
        validate = requests.get(uri).json()
        # TODO: So what happens if the token does not exist?
        if int(validate.get('expires_in')) > 0 and validate.get('email_verified') == 'true':
            return jsonify({'result': True, 'message': 'success'})
        else:
            return jsonify({'result': False, 'message': 'Token not valid'})
    except:
        print('Failed to decode')
        return jsonify({'result': False, 'message': 'token is invalid'})


class AccessToken:
    pass
