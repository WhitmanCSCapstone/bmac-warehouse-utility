import glob
import json
import csv
import os

# get json files
json_files = glob.glob("./stub_json/*.json")

# clean up the names
file_names = []
for name in json_files:
    file_names.append(name[12:-5])

def parseShipments(data):

    entries = data["shipments"]

    for entry in entries:

        # when stupid "ship_items" is literally nothing
        if(entry["ship_items"] == ''):
            entry["ship_items"] = []
            break

        items = entry["ship_items"].split(",")
        new_items = []
        for item in items:

            # product: case lots: tot weight
            values = item.split(":")
            keys = ["product", "case_lots", "total_weight"]

            # product; unit weight: case lots: total weight
            if(";" in values[0]):
                values = values[0].split(';') + values[1:3]
                keys = ['product', 'unit_weight', 'case_lots', 'total_weight']

            json_dict = {keys[i] : values [i] for i in range(len(keys))}
            new_items.append(json_dict)

        entry["ship_items"] = new_items

    data["shipments"] = entries

    return data


for json_file in json_files:
    if json_file[12:-5] == "Shipments":
        file = open(json_file, 'r')
        data = json.loads(file.read())
        file.close()

        new_data = parseShipments(data)

        with open(json_file, 'w') as outfile:
            json.dump(new_data, outfile)
