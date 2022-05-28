from pynamodb.attributes import UnicodeAttribute
from app.services.aws.dynamodb import BaseModel


class Config(BaseModel):

    class Meta(BaseModel.Meta):
        pass

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True, attr_name='sk')

    @staticmethod
    def setup_model(model, table_name):
        model.Meta.table_name = table_name
