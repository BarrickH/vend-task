from pynamodb.models import Model
from app.config.base import BaseConfig
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute,NumberAttribute, ListAttribute, MapAttribute


class BaseModel(Model):
    class Meta:
        region = BaseConfig.AWS_REGION
        aws_access_key_id = BaseConfig.AWS_ACCESS_KEY_ID
        aws_secret_access_key = BaseConfig.AWS_SECRET_ACCESS_KEY
        table_name = "Base.{}.{}".format(BaseConfig.PROJECT_NAME, BaseConfig.ENV)
        read_capacity_units = 5
        write_capacity_units = 5

        def __iter__(self):
            for attr, value in self.__dict__.items():
                yield attr, value

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            if isinstance(attr, MapAttribute):
                attr = getattr(self, name)
                if attr is None:
                    yield name, {}
                else:
                    yield name, getattr(self, name).as_dict()
            elif isinstance(attr, ListAttribute):
                attr = getattr(self, name)
                if attr is None:
                    yield name, []
                else:
                    items = [el.attribute_values
                             if isinstance(el, MapAttribute)
                             else el for el in attr]
                    yield name, items
            elif isinstance(attr, UTCDateTimeAttribute):
                if getattr(self, name):
                    yield name, attr.serialize(getattr(self, name))
            elif isinstance(attr, NumberAttribute):
                yield name, getattr(self, name)
            else:
                yield name, attr.serialize(getattr(self, name))


class ProductMeta(Model):
    class Meta:
        table_name=''
        pass

    def __init__(self, **attrs):
        super().__init__(**attrs)
        base_meta = [a for a in dir(BaseModel.Meta) if not a.startswith('__') and not callable(getattr(BaseModel.Meta, a))]
        for attr in base_meta:
            if attr != 'table_name':
                setattr(ProductMeta.Meta, attr, getattr(BaseModel.Meta,attr))


class OrderMeta(Model):
    class Meta:
        pass

    def __init__(self):
        super().__init__()
        base_meta = [a for a in dir(BaseModel.Meta) if not a.startswith('__') and not callable(getattr(BaseModel.Meta, a))]
        for attr in base_meta:
            if attr != 'table_name':
                setattr(ProductMeta.Meta, attr, getattr(BaseModel.Meta,attr))


class PkIdIndex(GlobalSecondaryIndex):
    class Meta(ProductMeta.Meta):
        index_name = "pk-id-index"
        projection = AllProjection()

    pk = UnicodeAttribute(hash_key=True)
    id = NumberAttribute(range_key=True)


class PkIdIndexOrder(GlobalSecondaryIndex):
    class Meta(OrderMeta.Meta):
        index_name = "pk-id-index"
        projection = AllProjection()

    pk = UnicodeAttribute(hash_key=True)
    id = NumberAttribute(range_key=True)


class NameCreateAtIndex(GlobalSecondaryIndex):
    class Meta(ProductMeta.Meta):
        index_name = "name-create_at-index"
        projection = AllProjection()

    name = UnicodeAttribute(hash_key=True)
    create_at = UTCDateTimeAttribute(range_key=True)