from pynamodb.models import Model
from app.config.base import BaseConfig
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute


class BaseModel(Model):
    class Meta:
        region = BaseConfig.AWS_REGION
        aws_access_key_id = BaseConfig.AWS_ACCESS_KEY_ID
        aws_secret_access_key = BaseConfig.AWS_SECRET_ACCESS_KEY
        table_name = "Base.{}.{}".format(BaseConfig.PROJECT_NAME, BaseConfig.ENV)


class NameCreateAtIndex(GlobalSecondaryIndex):
    class Meta(BaseModel.Meta):
        index_name = "name-create_at-index"
        projection = AllProjection()

    name = UnicodeAttribute(hash_key=True)
    create_at = UTCDateTimeAttribute(range_key=True)