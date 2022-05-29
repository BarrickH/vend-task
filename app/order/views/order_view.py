from flask_restful import Resource, abort, request, reqparse
from flask_apispec.views import MethodResource
from marshmallow import fields, Schema
from flask_apispec import use_kwargs, marshal_with, doc
from app.ultilities.auth.authenticator import api_auth
from app.order.models.order_model import OrderModel
from app.order.helpers.order_helpers import Sales


currency_const = {'USD': "$"}


class LineItemSchema(Schema):
    id = fields.Int()
    price = fields.Str(required=False)
    discount_percentage= fields.Float(required=False)
    quantity = fields.Int()


class OrderViewRequestSchema(Schema):
    line_items = fields.List(fields.Nested(LineItemSchema))
    discount_total_set = fields.Dict()


class OrderViewResponseSchema(Schema):
    id = fields.Int()
    price_total = fields.Float()

    line_items = fields.List(fields.Nested(LineItemSchema))
    discount_total_set = fields.Dict()


class OrderView(MethodResource):
    # create new products
    @api_auth
    @doc(description='Sales for Vend task', tags=['sale'])
    @use_kwargs(OrderViewRequestSchema, location='json')
    @marshal_with(OrderViewResponseSchema(partial=True))
    def post(self, tenant_id: str, **kwargs):
        Sales(tenant_id).create_sale_main(kwargs)
        Order = OrderModel()
        product.price_set = {"price": kwargs.get('price'), 'currency_code': currency_code}
        product.pk = kwargs.get('product_type') if kwargs.get('product_type') else 'simple'
        rs = product.save_product()
        return self.response_payload(rs)

    def response_payload(self, rs: OrderModel):
        price_with_currency = self.convert_price_set(rs.price_set)
        return {
            'id': rs.id,
            'name': rs.name,
            'price': price_with_currency
        }

    @staticmethod
    def convert_price_set(price_set: dict):
        return f"{currency_const[price_set.currency_code]}{price_set.price}"
