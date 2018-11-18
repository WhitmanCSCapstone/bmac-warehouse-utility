import json
import glob
import csv
import os
import subprocess

field_names = {
    "Customers": [
        "customer_id",
        "code",
        "address",
        "city",
        "state",
        "zip",
        "county",
        "contact",
        "phone",
        "email",
        "status",
        "notes"
    ],

    "FundingSources": [
        "id",
        "code"
    ],

    "Persons": [
        "unique_id",
        "username",
        "last_name",
        "first_name",
        "address",
        "city",
        "state",
        "zip",
        "phone1",
        "phone2",
        "email",
        "type",
        "status",
        "notes",
        "password",
    ],

    "Products": [
        "product_id",
        "product_code",
        "funding_source",
        "unit_weight",
        "unit_price",
        "initial_date",
        "initial_stock",
        "minimum_stock",
        "history",
        "current_stock",
        "inventory_date",
        "status",
        "notes"
    ],

    "Providers": [
        "provider_id",
        "code",
        "type",
        "address",
        "city",
        "state",
        "zip",
        "county",
        "contact",
        "phone",
        "email",
        "status",
        "notes"
    ],

    "Shipments": [
        "customer_id",
        "funds_source",
        "ship_date",
        "ship_via",
        "ship_items",
        "ship_rate",
        "total_weight",
        "total_price",
        "invoice_date",
        "invoice_no",
        "notes"
    ],

    "Contributions": [
        "provider_id",
        "recieve_date",
        "receive_items",
        "payment_source",
        "billed_amt",
        "notes"
    ],
}

# get csv files
csv_files = glob.glob("./stub_csvs/*.csv")

# clean up the names
file_names = []
for name in csv_files:
    file_names.append(name[12:-4])

# erase all the previously written json files
for name in file_names:
    open("./stub_json/{}.json".format(name), "w").close()

# write new json from csv files
for f in csv_files:

    csv_file = open(f, "r")
    clean_name = f[12:-4]

    reader = csv.DictReader(csv_file, field_names[clean_name])

    json_file = open("./stub_json/{}.json".format(clean_name), 'w+')
    json_file.write("{" + '"{}": ['.format(clean_name.lower()))

    for row in reader:
        json.dump(row, json_file)
        json_file.write(",")

    # make it valid json (SUPER janky)
    json_file.close()

    json_file = open("./stub_json/{}.json".format(clean_name), 'rb+')
    json_file.seek(-1, os.SEEK_END)
    json_file.truncate()
    json_file.close()

    json_file = open("./stub_json/{}.json".format(clean_name), 'a')
    json_file.write("]}")
    json_file.close()
    csv_file.close()

print("CSV files have been converted to JSON!")

cmd = ['python', 'fix_json.py']
subprocess.Popen(cmd).wait()
print("JSON files have been rewritten and fixed!")

cmd = ['python', 'provider_refactor.py']
subprocess.Popen(cmd).wait()
print("Providers.json has been refactored!")


# get all the new json files
json_files = glob.glob("./stub_json/*.json")

obj_list = []

# compile json files into one json object
for f in json_files:
    with open(f, 'rb') as data:
        obj = json.load(data)
        obj_list.append(obj)

# erase the contents of the old file
open("master_json.json", "w").close()

# write the compiled json to master_json.json
with open("master_json.json", "w") as outfile:
    json.dump(obj_list, outfile, indent=4, sort_keys=True)


print("master_json.json has been updated!")
