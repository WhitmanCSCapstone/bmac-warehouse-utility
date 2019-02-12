import json
import uuid

# FIRST FIX PROVIDERS

file_name = './stub_json/Providers.json'

file = open(file_name, 'r')
data = json.loads(file.read())
file.close()

providers = data['providers']

new_dict = {'providers': {}}

provider_id_to_hash_map = {}

counter = 0

for provider in providers:
    uniq_id = uuid.uuid5(uuid.NAMESPACE_OID, str(provider))
    new_dict['providers'][str(uniq_id)] = provider

    provider['uniq_id'] = str(uniq_id)

    name = provider['provider_id']
    # b/c whoever designed this made the provider_id in a receipts object only have the name, not the location, so we can't know if the old data meant that this receipts was from the alberstons in King County or in Walla Walla, so I'm arbitrarily choosing the one that I loop over first to be the one that gets the receipt credit
    if name not in provider_id_to_hash_map:
        provider_id_to_hash_map[name] = str(uniq_id)
    else:
        counter += 1

print('There are {} duplicate providers in the providers table'.format(counter))

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

for receipt in receipts:
    name = receipt['provider_id']
    try:
        uniq_id = provider_id_to_hash_map[name]
    except:
        counter += 1
        uniq_id = 'INVALID PROVIDER ID'
    receipt['provider_id'] = uniq_id
    new_dict['contributions'].append(receipt)

print('{} receipts have provider_ids listed that do not exist in the providers table'.format(counter))

with open(file_name, 'w') as outfile:
    json.dump(new_dict, outfile)
