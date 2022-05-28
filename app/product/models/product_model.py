from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, MapAttribute
from app.services.aws.dynamodb import BaseModel, NameCreateAtIndex
from datetime import datetime
from app.ultilities.helpers import get_instance_id


class ProductModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    pk = UnicodeAttribute(hash_key=True)
    sk = NumberAttribute(range_key=True)
    # Global Secondary Index
    name_create_at_index = NameCreateAtIndex()
    # identifier = bc email
    name = UnicodeAttribute(null=False)
    price_set = MapAttribute(null=True)
    create_at = UTCDateTimeAttribute()

    @staticmethod
    def set_hash_key(product_type: str = 'simple'):
        return 'Product__{}'.format(product_type)

    def save_product(self):
        if not self.pk.startswith('Product__'):
            self.pk = self.set_hash_key(self.pk)
        if not self.create_at:
            self.create_at = datetime.utcnow()
        if not self.sk:
            product_id = get_instance_id(self.pk, ProductModel)
            self.sk = product_id
        super(ProductModel, self).save()
        return self
