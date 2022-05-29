from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute, UTCDateTimeAttribute, MapAttribute
from app.services.aws.dynamodb import BaseModel, NameCreateAtIndex, PkIdIndex
from datetime import datetime
from app.ultilities.helpers import get_instance_new_id


class OrderModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    # Global Secondary Index
    pk_id_index = PkIdIndex()
    id = NumberAttribute(null=False)

    line_items = ListAttribute(of=MapAttribute,null=True)
    create_at = UTCDateTimeAttribute()

    # those methods could make public method and move to base model, so that other resource could utilize
    @staticmethod
    def set_hash_key():
        return 'Order'

    def save_order(self):
        if not self.pk != 'Order':
            self.pk = self.set_hash_key(self.pk)
        if not self.create_at:
            self.create_at = datetime.utcnow()
        if not self.sk:
            order_id = get_instance_new_id(self.pk, self)
            self.sk = str(order_id)
            self.id = order_id

        super(OrderModel, self).save()
        return self
