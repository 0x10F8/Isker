import seed
from data import filestore

if not filestore.do_files_exist():
    seed.seed_data_store()

# Get all the region ids
regions_ids = filestore.load_region_ids()

# Get region info
region_infos = filestore.load_region_info()

# Get market data for each region
market_datas = filestore.load_market_data()

# Create a list of all the unique market location ids
location_ids = filestore.load_location_ids()

# Get the location information
locations = filestore.load_location_info()

# Get all the buy and sell orders
buy_orders = filestore.load_buy_orders()
sell_orders = filestore.load_sell_orders()

# Item type ids
type_ids = filestore.load_type_ids()

# Get the item information
types = filestore.load_type_info()

# Map the orders to the type of item
buy_orders_by_type = {order['type_id']: order for order in buy_orders}
sell_orders_by_type = {order['type_id']: order for order in sell_orders}
