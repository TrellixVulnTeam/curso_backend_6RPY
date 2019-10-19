import os
import jwt
from dotenv import load_dotenv
from pathlib import Path
from flask import json
from functools import wraps
from flask import request, jsonify


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



def handler_response(app, code_error, output, payload = None):
    if payload is None:
        payload = {}
    response_object = {
        'response': {
            'systemMessage': output,
            'apiResponse': payload,
            'statusCode': code_error,
        }
    }

    response = app.response_class(
        response = json.dumps(response_object),
        status = code_error,
        mimetype = 'application/json'
    )

    return response

def jwt_secret():
    return os.getenv('JWT_SECRET')

def token_required(f):
    @wraps(f)
    def decorator(*ars, **kwargs):
        token = request.headers.get('_token')
        if not token:
            return jsonify({
                'response': {
                    'systemMessage': 'Token no encontrado',
                    'apiResponse': {},
                    'statusCode': 401,
                }
            }), 401

        try:
            jwt.decode(token, jwt_secret())
        except Exception as e:
            return jsonify({
                'response': {
                    'systemMessage': 'Token incorrecto',
                    'apiResponse': {'error': f'{str(e)}'},
                    'statusCode': 401,
                }
            }), 401
        return f(*ars, **kwargs)
    return decorator

def token_get_object():
    token = request.headers.get('_token')
    objeto = jwt.decode(token.encode('utf-8'), jwt_secret())
    return objeto