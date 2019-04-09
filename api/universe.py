from api import api

STATION_ID_LIMIT = 1000000000000


def get_region_ids():
    return api.do_get(1, 'universe/regions', {})


def get_region_info(id):
    return api.do_get(1, 'universe/regions/' + str(id), {})


def get_system_ids():
    return api.do_get(1, 'universe/systems', {})


def get_system_info(id):
    return api.do_get(4, 'universe/systems/' + str(id), {})


def get_station_info(id):
    return api.do_get(2, 'universe/stations/' + str(id), {})


def get_structure_info(id):
    return api.do_get(2, 'universe/structures/' + str(id), {})


def get_type_info(id):
    return api.do_get(3, 'universe/types/' + str(id), {})
