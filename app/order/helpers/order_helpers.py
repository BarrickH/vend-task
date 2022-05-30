from app.order.models.order_model import OrderModel
from app.product.models.product_model import ProductModel
from flask_restful import abort

from app.ultilities.helpers import get_instance_new_id


def get_product_record(tenant_id: str, pid: int, pm: ProductModel):
    try:
        return pm.get(hash_key=ProductModel.set_hash_key(), range_key=str(pid))
    except Exception as e:
        abort(400, msg=f'product not found (id: {pid})')


class Sales:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.product_model = ProductModel()
        self.product_model.set_model(tenant_id=tenant_id)
        self.order_model = OrderModel()
        self.order_model.set_model(tenant_id=tenant_id)

    def create_sale_main(self, payload):
        # 1. get line item price from data base
        line_items = self.acquire_sale_prices(payload.get('line_items'))
        # 2. get price total
        price_total = 0
        for l in line_items:
            try:
                price_total += self.calculate_each_line(price=float(l.get('price_set').get('price')),
                                                        qty=int(l.get('quantity')))
            except Exception as e:
                abort(400, msg='product quantity can not less than 1')
        # 3. save to db and return
        order_payload = {'line_items': line_items, 'price_total': price_total}
        rs = self.save_order(order_payload)
        order_payload['id'] = rs.id
        order_payload['tenant_id'] = self.tenant_id
        return order_payload

    def acquire_sale_prices(self, items):
        product_records = [get_product_record(self.tenant_id, i.get('id'), self.product_model) for i in items]
        for p in product_records:
            for i in items:
                if str(p.id) == str(i.get('id')):
                    i.update(dict(p))
                    break
        return items

    def calculate_each_line(self, price: float, qty: int):
        if qty <= 0:
            raise Exception('')
        return float(price) * int(qty)

    def save_order(self, payload):
        for attr, val in payload.items():
            setattr(self.order_model, attr, val)
        return self.order_model.save_order()
