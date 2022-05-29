from flask_restful import Resource, abort, request, reqparse
from flask_apispec.views import MethodResource
from marshmallow import fields, Schema
from flask_apispec import use_kwargs, marshal_with, doc
from app.ultilities.auth.authenticator import api_auth
from app.product.models.product_model import ProductModel, StoreModel

currency_const = {'USD':"$"}


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
        rs = ProductModel.pk_id_index.query(hash_key=ProductModel.set_hash_key(), limit=kwargs.get('size'),
                                last_evaluated_key=kwargs.get('cursor'), scan_index_forward=kwargs.get('after'))
        return [self.response_payload(r) for r in rs if r]

    # create new products
    @api_auth
    @doc(description='Product for Vend task', tags=['Product'])
    @use_kwargs({'name': fields.Str(required=True),
                 'price': fields.Str(required=True),
                 'currency_code': fields.Str(required=False),
                 'product_type': fields.Str(required=False)},
                location='json')
    @marshal_with(ProductViewSchema)
    def post(self, tenant_id:str,**kwargs):
        product = ProductModel()
        product.name = kwargs.get('name')
        currency_code = kwargs.get('currency_code')
        if not currency_code:
            try:
                currency_code = StoreModel.get(hash_key=StoreModel.set_hash_key(tenant_id),
                                               range_key=StoreModel.set_sort_key('currency_code')).value
            except Exception as e:
                print(str(e))
                abort(500, msg='internal server error')

        if currency_code.upper() not in currency_const.keys():
            raise Exception
        product.price_set = {"price":kwargs.get('price'),'currency_code': currency_code}
        product.pk = kwargs.get('product_type') if kwargs.get('product_type') else 'simple'
        rs = product.save_product()
        return self.response_payload(rs)

    def response_payload(self,rs:ProductModel):
        price_with_currency = self.convert_price_set(rs.price_set)
        return {
            'id': rs.id,
            'name': rs.name,
            'price': price_with_currency
        }

    @staticmethod
    def convert_price_set(price_set:dict):
        return f"{currency_const[price_set.currency_code]}{price_set.price}"
