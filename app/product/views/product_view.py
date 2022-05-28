from flask_restful import Resource, abort, request, reqparse
from flask_apispec.views import MethodResource
from marshmallow import fields, Schema
from flask_apispec import use_kwargs, marshal_with, doc
from app.ultilities.auth.authenticator import api_auth
from app.product.models.product_model import ProductModel


const = {
            'USD':"$"
        }


class ProductViewSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Str()


class ProductView(MethodResource):

    # query all products with pagination
    @api_auth
    @doc(description='Product for Vend task', tags=['Product'])
    @use_kwargs({'cursor': fields.Str(required=False),
                 'size': fields.Str(required=False),
                 'after': fields.Bool(required=False)},
                location='query')
    @marshal_with(ProductViewSchema(many=True))
    def get(self, **kwargs):
        rs = ProductModel.query(hash_key=ProductModel.set_hash_key(), limit=kwargs.get('size'),
                                last_evaluated_key=kwargs.get('cursor'), scan_index_forward=kwargs.get('after'))
        return [self.response_payload(r) for r in rs]

    # create new products
    @api_auth
    @doc(description='Product for Vend task', tags=['Product'])
    @use_kwargs({'name': fields.Str(required=True),
                 'price': fields.Str(required=True),
                 'currency_code': fields.Str(required=False)},
                location='json')
    @marshal_with(ProductViewSchema)
    def post(self, **kwargs):
        try:
            ProductModel.name = kwargs.get('name')
            ProductModel.price_set = {"price":kwargs.get('price'),'currency_code': kwargs.get('currency_code')}
            rs = ProductModel().save_product()
            return self.response_payload(rs)
        except Exception as e:
            print(str(e))
            abort(400, msg='data format error')

    def response_payload(self,rs:ProductModel):
        price_with_currency = self.convert_price_set(rs.price_set)
        return {
            'ID': rs.sk,
            'Name': rs.name,
            'Price': price_with_currency
        }

    @staticmethod
    def convert_price_set(price_set:dict):
        return f"{const[price_set.get('currency_code')]}{price_set.get('price')}"
