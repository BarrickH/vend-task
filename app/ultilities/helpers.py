from pynamodb.models import Model


def get_instance_new_id(pk: str, model_instance: Model):
    try:
        # should change to PkIntityIdIndex later
        rs = model_instance.pk_id_index.query(hash_key=pk, scan_index_forward=False, limit=1)
    except Exception as e:
        print(e)
        return 1
    else:
        try:
            for m in rs:
                # should change to intity_id
                return m.id + 1
        except Exception as e:
            print(e)
        return 1
