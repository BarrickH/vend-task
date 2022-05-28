from pynamodb.models import Model


def get_instance_id(pk: str, model_instance: Model):
    rs = model_instance.query(hash_key=pk, scan_index_forward=False, limit=1)
    for m in rs:
        return m.sk + 1
    return 1
