from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, MapAttribute
from app.services.aws.dynamodb import BaseModel, NameCreateAtIndex, PkIdIndex, ProductMeta
from datetime import datetime
from app.ultilities.helpers import get_instance_new_id
from app.config.base import BaseConfig


class ProductModel(ProductMeta):
    class Meta(ProductMeta.Meta):
        # table_name = "vend_barrick.vend_demo.development"
        pass

    @staticmethod
    def set_model(tenant_id:str=None):
        if not ProductMeta.Meta.table_name:
            ProductMeta.Meta.table_name = "{}.{}.{}".format(tenant_id, BaseConfig.PROJECT_NAME,
                                                            BaseConfig.ENV)

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    # Global Secondary Index
    pk_id_index = PkIdIndex()
    name_create_at_index = NameCreateAtIndex()

    id = NumberAttribute(null=False)
    name = UnicodeAttribute(null=False)
    price_set = MapAttribute(null=True)
    create_at = UTCDateTimeAttribute()

    # those methods could make public method and move to base model, so that other resource could utilize
    @staticmethod
    def set_hash_key(product_type: str = 'simple'):
        return 'Product__{}'.format(product_type)

    def save_product(self):
        if not self.pk.startswith('Product__'):
            self.pk = self.set_hash_key(self.pk)
        if not self.create_at:
            self.create_at = datetime.utcnow()
        if not self.sk:
            product_id = get_instance_new_id(self.pk, self)
            self.sk = str(product_id)
            self.id = product_id

        super(ProductModel, self).save()
        return self


# move out from product model to config model
class StoreModel(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    # pk = Config__tenant_id
    pk = UnicodeAttribute(hash_key=True)
    # sk = store_default__currency_code
    sk = UnicodeAttribute(range_key=True)
    value = UnicodeAttribute(null=False)

    @staticmethod
    def set_hash_key(tenant_id: str):
        return 'Config__{}'.format(tenant_id)

    @staticmethod
    def set_sort_key(key: str):
        return 'store_default__{}'.format(key)
