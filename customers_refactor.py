import json
import uuid

# FIRST FIX Customers

file_name = './stub_json/Customers.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

customers = data['customers']

new_dict = {'customers': {}}

customer_id_to_hash_map = {}

counter = 0

for customer in customers:
    uniq_id = uuid.uuid5(uuid.NAMESPACE_OID, str(customer))
    new_dict['customers'][str(uniq_id)] = customer

    customer['uniq_id'] = str(uniq_id)

    name = customer['customer_id']
    # b/c whoever designed this made the provider_id in a receipts object only have the name, not the location, so we can't know if the old data meant that this receipts was from the alberstons in King County or in Walla Walla, so I'm arbitrarily choosing the one that I loop over first to be the one that gets the receipt credit
    if name not in customer_id_to_hash_map:
        customer_id_to_hash_map[name] = str(uniq_id)
    else:
        counter += 1

print('There are {} duplicate customers in the customers table'.format(counter))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)

# NOW FIX Shipments W/NEW Customer IDS

file_name = './stub_json/Shipments.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

shipments = data['shipments']

new_dict = {'shipments': []}

counter = 0

for shipment in shipments:
    name = shipment['customer_id']
    try:
        uniq_id = customer_id_to_hash_map[name]
    except:
        counter += 1
        uniq_id = 'INVALID CUSTOMER ID'
    shipment['customer_id'] = uniq_id
    new_dict['shipments'].append(shipment)

print('{} shipments have customer_ids listed that do not exist in the customers table'.format(counter))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)
