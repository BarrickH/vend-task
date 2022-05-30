from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute, UTCDateTimeAttribute, MapAttribute
from app.services.aws.dynamodb import OrderMeta, NameCreateAtIndex, PkIdIndexOrder
from datetime import datetime
from app.ultilities.helpers import get_instance_new_id
from app.config.base import BaseConfig


class OrderModel(OrderMeta):
    class Meta(OrderMeta.Meta):
        pass

    @staticmethod
    def set_model(tenant_id: str = None):
        if not OrderModel.Meta.table_name:
            OrderModel.Meta.table_name = "{}.{}.{}".format(tenant_id, BaseConfig.PROJECT_NAME,
                                                           BaseConfig.ENV)

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    # Global Secondary Index
    pk_id_index = PkIdIndexOrder()
    id = NumberAttribute(null=False)
    price_total = UnicodeAttribute(default="0")
    line_items = ListAttribute(of=MapAttribute, null=True)
    # just for convenient. list might be more fit in real task
    discount_total_set = MapAttribute(null=True)
    create_at = UTCDateTimeAttribute()

    # those methods could make public method and move to base model, so that other resource could utilize
    @staticmethod
    def set_hash_key():
        return 'Order'

    def save_order(self):
        if self.pk != 'Order':
            self.pk = self.set_hash_key()
        if not self.create_at:
            self.create_at = datetime.utcnow()
        if not self.sk:
            order_id = get_instance_new_id(self.pk, self)
            self.sk = str(order_id)
            self.id = order_id

        super(OrderModel, self).save()
        return self
