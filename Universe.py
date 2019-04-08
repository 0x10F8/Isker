import api


def get_region_ids():
    return api.do_get(1, 'universe/regions', {})


def get_region_info(id):
    return api.do_get(1, 'universe/regions/' + str(id), {})


def get_system_ids():
    return api.do_get(1, 'universe/systems', {})


def get_system_info(id):
    return api.do_get(4, 'universe/systems/' + str(id), {})


for id in get_system_ids():
    print(get_system_info(id))
