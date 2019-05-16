import json
import uuid

# FIRST FIX Products

file_name = './stub_json/Products.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

products = data['products']

new_dict = {'products': {}}

product_id_to_hash_map = {}

counter = 0

for key in products:

    product = products[key]
    uniq_id = key

    new_dict['products'][str(uniq_id)] = product

    product['uniq_id'] = str(uniq_id)

    name = product['product_id']

    if name not in product_id_to_hash_map:
        product_id_to_hash_map[name] = str(uniq_id)
    else:
        counter += 1

print('There are {} products in the products table with duplicate product_ids'.format(counter))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)

# NOW FIX Shipments W/NEW Product IDS

file_name = './stub_json/Shipments.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

shipments = data['shipments']

new_dict = {'shipments': {}}

counter = 0

for key in shipments:
    items = shipments[key]['ship_items']
    for item in items:
        name = item['product']

        try:
            uniq_id = product_id_to_hash_map[name]
        except:
            counter += 1
            uniq_id = 'INVALID PRODUCT ID'

        item['product'] = uniq_id

    new_dict['shipments'][key] = shipments[key]

print('{} shipments have product_ids listed that do not exist in the products table'.format(counter))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)


# NOW FIX Receipts W/NEW Product IDS

file_name = './stub_json/Contributions.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

receipts = data['contributions']

new_dict = {'contributions': {}}

counter = 0

for key in receipts:
    items = receipts[key]['receive_items']
    for item in items:
        name = item['product']

        try:
            uniq_id = product_id_to_hash_map[name]
        except:
            counter += 1
            uniq_id = 'INVALID PRODUCT ID'

        item['product'] = uniq_id

    new_dict['contributions'][key] = receipts[key]

print('{} receipts have product_ids listed that do not exist in the products table'.format(counter))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)
