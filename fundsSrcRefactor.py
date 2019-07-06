import json
import uuid

# FIRST FIX Customers

file_name = './stub_json/FundingSources.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

fundingsources = data['fundingsources']

fundingsource_id_to_hash_map = {}

counter = 0

for key in fundingsources:
    uniq_id = key

    name = fundingsources[key]['id']
    # b/c whoever designed this made the provider_id in a receipts object only have the name, not the location, so we can't know if the old data meant that this receipts was from the alberstons in King County or in Walla Walla, so I'm arbitrarily choosing the one that I loop over first to be the one that gets the receipt credit
    if name not in fundingsource_id_to_hash_map:
        fundingsource_id_to_hash_map[name] = uniq_id;
    else:
        counter += 1

print('There are {} duplicate fundingsources in the fundingsources table'.format(counter))

# NOW FIX Shipments W/NEW Customer IDS

file_name = './stub_json/Shipments.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

shipments = data['shipments']

new_dict = {'shipments': []}

counter = 0

for key in shipments:
    shipment = shipments[key]
    name = shipment['funds_source']
    try:
        uniq_id = fundingsource_id_to_hash_map[name]
    except:
        counter += 1
        uniq_id = 'INVALID FUNDING SOURCE ID'
    shipment['funds_source'] = uniq_id
    new_dict['shipments'].append(shipment)

print('{} shipments have funding sources listed that do not exist in the funding sources table'.format(counter))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)


# NOW FIX CONTRIBUTIONS W/NEW PROVIDER IDS

file_name = './stub_json/Contributions.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

receipts = data['contributions']

new_dict = {'contributions': []}

counter = 0

for key in receipts:
    receipt = receipts[key]
    name = receipt['payment_source']
    try:
        uniq_id = fundingsource_id_to_hash_map[name]
    except:
        counter += 1
        uniq_id = 'INVALID FUNDING SOURCE ID'
    receipt['payment_source'] = uniq_id
    new_dict['contributions'].append(receipt)

print('{} receipts have funding sources listed that do not exist in the funding sources table'.format(counter))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)

# then do products


file_name = './stub_json/Products.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

products = data['products']

new_dict = {'products': []}

counterA = 0
counterB = 0

for key in products:
    product = products[key]
    name = product['funding_source']
    try:
        print(name)
        counterA += 1
        uniq_id = fundingsource_id_to_hash_map[name]
    except:
        counterB += 1
        uniq_id = 'INVALID FUNDING SOURCE ID'
    product['funding_source'] = uniq_id
    new_dict['products'].append(product)

print('out of {} products, {} products have funding sources listed that do not exist in the funding sources table, and {} do'.format(counterA + counterB, counterB, counterA))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)
