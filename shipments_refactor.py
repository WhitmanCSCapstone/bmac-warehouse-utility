import json
import uuid
import glob


def give_uniq_ids(file_name, key):

    file = open(file_name, 'r')
    data = json.loads(file.read())
    file.close()

    objects = data[key]

    new_dict = {key: {}}

    for obj in objects:
        uniq_id = uuid.uuid5(uuid.NAMESPACE_OID, str(obj))

        # make objs self-referential
        obj['uniq_id'] = str(uniq_id)

        new_dict[key][str(uniq_id)] = obj

    with open(file_name, 'w') as outfile:
        json.dump(new_dict, outfile)


# get all the new json files
json_files = glob.glob("./stub_json/*.json")

for file_name in json_files:
    if "Customers" not in file_name and "Providers" not in file_name:
        key = file_name[12:-5].lower()
        give_uniq_ids(file_name, key)
