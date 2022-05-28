from pynamodb.models import Model


def get_instance_id(pk: str, model_instance: Model):
    try:
        rs = model_instance.query(hash_key=pk, scan_index_forward=False, limit=1)
    except Exception as e:
        print(e)
        return 1
    else:
        try:
            for m in rs:
                return str(int(m.sk) + 1)
        except Exception as e:
            print(e)
        return 1
