import Api


def get_region_ids():
    response = Api.do_get('universe/regions', {})
    return response


print(get_region_ids())
