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

def parseItems(data, table_name, accessor):
    """function that takes a json object, a table name, and an accessor key and parses the items from strings to arrays of json objects"""

    entries = data[table_name.lower()]

    for entry in entries:

        # edge case
        if(entry[accessor] == ''):
            entry[accessor] = []
            continue

        items = entry[accessor].split(",")
        new_items = []

        for item in items:
            # product: case lots: tot weight
            values = item.split(":")
            keys = ["product", "case_lots", "total_weight"]
            # if no data except for product name
            if(":" not in item):
                keys = ["product"]
            if(";" in values[0]):
                values = values[0].split(';') + values[1:3]
                # product; unit weight: case lots: total weight
                if(len(values) == 4):
                    keys = ['product', 'unit_weight', 'case_lots', 'total_weight']
                # product; funds_source; unit weight: case lots: total weight
                elif(len(values) == 5):
                    keys = ['product', 'funds_source', 'unit_weight', 'case_lots', 'total_weight']
                # product; funds_source; unit weight; unit weight dupe: case lots: total weight
                elif(len(values) == 6):
                    keys = ['product', 'funds_source', 'unit_weight', 'case_lots', 'total_weight']
                    firstUW = values[2] if values[2] != '' and values[2] != ' ' else False
                    secondUW = values[3] if values[3] != '' and values[3] != ' ' else False

                    if(firstUW or secondUW):
                        if(firstUW and secondUW):
                            values[2] = max(int(firstUW, 10), int(secondUW, 10))
                        else:
                            values[2] = firstUW if firstUW else secondUW
                    else:
                        values[2] = ''

                    values[3] = values[4]
                    values[4] = values[5]

            # create the new item as a dict
            json_dict = {keys[i] : values [i] for i in range(len(keys))}
            new_items.append(json_dict)

        entry[accessor] = new_items

    data[table_name.lower()] = entries

    return data


for json_file in json_files:

    clean_name = json_file[12:-5]

    if clean_name == "Shipments":
        file = open(json_file, 'r')
        data = json.loads(file.read())
        file.close()
        new_data = parseItems(data, clean_name, "ship_items")
        with open(json_file, 'w') as outfile:
           json.dump(new_data, outfile)

    elif clean_name == "Contributions":
        file = open(json_file, 'r')
        data = json.loads(file.read())
        file.close()
        new_data = parseItems(data, clean_name, "receive_items")
        with open(json_file, 'w') as outfile:
           json.dump(new_data, outfile)
