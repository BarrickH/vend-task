from app.ultilities.auth.authenticator import JWTAuth
from flask_apispec import use_kwargs
from marshmallow import fields
from flask_apispec.views import MethodResource


class Auth(MethodResource):
    def __init__(self):
        pass

    @use_kwargs({'client_id': fields.Str(required=True),
                 'client_secret': fields.Str(required=True)},
                location='json')
    def post(self, tenant_id:str, **kwargs):
        token = JWTAuth().generate_token(tenant_id=tenant_id, client_id=kwargs.get('client_id'), secret=
        kwargs.get('client_secret'), expiry_time=3600)
        return{
            "token_type": "Bearer",
            "expires_in": "3599",
            "access_token": token
        }