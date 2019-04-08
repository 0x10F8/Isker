import Api


def get_region_ids():
    response = Api.do_get('universe/regions', {})
    return response


def get_region_info(id):
    response = Api.do_get('universe/regions/' + str(id), {})
    return response


for id in get_region_ids():
    print(get_region_info(id))
