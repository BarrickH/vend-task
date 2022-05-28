from app.ultilities.auth.authenticator import JWTAuth
from flask_apispec import use_kwargs
from marshmallow import fields


class Auth:
    def __init__(self):
        pass

    @use_kwargs({'UmbracoOrderNumber': fields.Str(required=True),
                 'PackingSlipId': fields.Str(required=False),
                 'SalesOrderId': fields.Str(required=False),
                 'WebShopCustomerId': fields.Str(required=False)},
                location='json')
    def post(self, **kwargs):
        return JWTAuth().generate_token(tenant_id=kwargs.get('tenant_id'), client_id=kwargs.get('client_id'), secret=
        kwargs.get('secret'), expiry_time=3600)
