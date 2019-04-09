import json
import os

REGION_IDS_FILE = 'REGION_IDS.json'
REGION_INFO_FILE = 'REGION_INFO.json'
MARKET_DATA_FILE = 'MARKET_DATA.json'
LOCATION_IDS_FILE = 'LOCATION_IDS.json'
LOCATION_INFO_FILE = 'LOCATION_INFO.json'
BUY_ORDERS_FILE = 'BUY_ORDERS.json'
SELL_ORDERS_FILE = 'SELL_ORDERS.json'
TYPE_IDS_FILE = 'TYPE_IDS.json'
TYPE_INFO_FILE = 'TYPE_INFO.json'

ALL_FILES = [REGION_IDS_FILE, REGION_INFO_FILE, MARKET_DATA_FILE, LOCATION_IDS_FILE, LOCATION_INFO_FILE,
             BUY_ORDERS_FILE, SELL_ORDERS_FILE, TYPE_IDS_FILE, TYPE_INFO_FILE]


def do_files_exist():
    exists = True
    for file in ALL_FILES:
        if not os.path.isfile(file):
            exists = False
    return exists


def store_json_object_to_file(object, file_name):
    json_object = json.dumps(object)
    file = open(file_name, 'w')
    file.write(json_object)
    file.close()


def load_object_from_json_file(file_name):
    file = open(file_name, 'r')
    json_object = file.read()
    file.close()
    return json.loads(json_object)


def store_type_ids(type_ids):
    store_json_object_to_file(type_ids, TYPE_IDS_FILE)


def load_type_ids():
    return load_object_from_json_file(TYPE_IDS_FILE)


def store_type_info(type_info):
    store_json_object_to_file(type_info, TYPE_INFO_FILE)


def load_type_info():
    return load_object_from_json_file(TYPE_INFO_FILE)


def store_sell_orders(sell_orders):
    store_json_object_to_file(sell_orders, SELL_ORDERS_FILE)


def load_sell_orders():
    return load_object_from_json_file(SELL_ORDERS_FILE)


def store_buy_orders(buy_orders):
    store_json_object_to_file(buy_orders, BUY_ORDERS_FILE)


def load_buy_orders():
    return load_object_from_json_file(BUY_ORDERS_FILE)


def store_region_ids(region_ids):
    store_json_object_to_file(region_ids, REGION_IDS_FILE)


def load_region_ids():
    return load_object_from_json_file(REGION_IDS_FILE)


def store_region_info(region_info):
    store_json_object_to_file(region_info, REGION_INFO_FILE)


def load_region_info():
    return load_object_from_json_file(REGION_INFO_FILE)


def store_market_data(market_data):
    store_json_object_to_file(market_data, MARKET_DATA_FILE)


def load_market_data():
    return load_object_from_json_file(MARKET_DATA_FILE)


def store_location_ids(location_ids):
    store_json_object_to_file(location_ids, LOCATION_IDS_FILE)


def load_location_ids():
    return load_object_from_json_file(LOCATION_IDS_FILE)


def store_location_info(location_info):
    store_json_object_to_file(location_info, LOCATION_INFO_FILE)


def load_location_info():
    return load_object_from_json_file(LOCATION_INFO_FILE)
