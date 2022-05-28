from flask import request, abort, current_app
from functools import wraps
from datetime import datetime, timedelta
from app.ultilities.auth.models.auth_model import AuthModel
import jwt
import uuid
import os


class JWTAuth:

    def __init__(self):
        # need to save to db later:
        self.issuer = os.getenv('OAUTH_ISSUER')

    def encode_token(self, audience, secret, expires_in: int):
        now = datetime.utcnow()
        return jwt.encode(
            payload={
                "ref": str(uuid.uuid4()),
                "aud": audience,
                "iss": self.issuer,
                "exp": now + timedelta(seconds=expires_in)
            },
            key=secret,
            algorithm='HS512'
        )

    def decode_token(self, tenant_id: str, token: str, verify=True):
        audience=''
        secret=''
        try:
            client = AuthModel.query(hash_key=AuthModel.set_hash_key(tenant_id))

        except Exception as e:
            print(str(e))
            return abort(500, msg='internal server error')
        else:
            for c in client:
                audience = c.sk
                secret = c.secret
        try:
            payload = jwt.decode(jwt=token, key=secret, audience=audience, verify=verify,
                                 algorithms=['HS512'])
        except jwt.ExpiredSignatureError:
            print('ExpiredSignatureError')
            raise Exception
        except jwt.InvalidTokenError:
            print('InvalidTokenError')
            raise Exception
        except Exception as e:
            print(str(e))
            raise Exception
        else:
            return payload

    def generate_token(self, tenant_id: str, client_id: str, secret: str, expiry_time: int):
        if self.verify_client_secret(tenant_id, client_id, secret):
            return self.encode_token(audience=client_id, secret=secret,
                                     expires_in=expiry_time).decode()
        abort(401)

    def verify_access_token(self, tenant_id: str, access_token: str):
        try:
            self.decode_token(tenant_id=tenant_id, token=access_token)
        except Exception as e:
            print(str(e))
            return False
        else:
            return True

    @staticmethod
    def verify_client_secret(tenant_id: str, client_id: str, secret: str):
        try:
            client = AuthModel.query(hash_key=AuthModel.set_hash_key(tenant_id))
        except Exception as e:
            print(str(e))
            abort(401)
        else:
            for c in client:
                if c.sk == client_id and c.secret == secret:
                    return True
        return False


def api_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        tenant_id = kwargs.get('tenant_id')
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                auth = auth_header.split(" ")
                if auth[0] != "Bearer":
                    raise IndexError
                else:
                    token = auth[1]
            except IndexError:
                abort(401)

        if not token:
            abort(401)

        verified = JWTAuth().verify_access_token(tenant_id, token)
        if verified:
            try:
                return f(*args, **kwargs)
            except TypeError:
                abort(400)
        else:
            abort(401)

    return decorated_function