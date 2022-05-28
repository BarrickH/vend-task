from pynamodb.attributes import UnicodeAttribute
from app.services.aws.dynamodb import BaseModel


class AuthModel(BaseModel):

    class Meta(BaseModel.Meta):
        pass

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    secret = UnicodeAttribute(null=False)

    @staticmethod
    def set_hash_key(tenant_id):
        return 'Client__{}'.format(tenant_id)