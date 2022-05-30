from app.order.models.order_model import OrderModel
from app.product.models.product_model import ProductModel
from flask_restful import abort


def get_product_record(tenant_id: str, pid: int):
    try:
        r = ProductModel(tenant_id=tenant_id).pk_id_index.get(hash_key=ProductModel.set_hash_key(tenant_id), range_key=pid)
    except Exception as e:
        abort(400, msg=f'product not found (id: {pid})')


class Sales:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def create_sale_main(self, payload):
        # 1. get line item price from data base
        line_items = self.acquire_sale_prices(payload.get('line_items'))
        # 2. get price total
        price_total = 0
        for l in line_items:
            try:
                price_total += self.calculate_each_line(price=float(l.get('price')),qty=int(l.get('quantity')))
            except Exception as e:
                abort(400, msg='product quantity can not less than 1')
        return {
            'line_items': line_items,
            'price_total': price_total
        }

    def acquire_sale_prices(self, items):
        product_records = [get_product_record(self.tenant_id, i.get('id')) for i in items]
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
